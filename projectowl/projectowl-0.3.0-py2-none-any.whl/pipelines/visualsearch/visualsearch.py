"""Visual search pipeline.
"""

import os
import time

import cPickle as pickle
import numpy as np

from tqdm import tqdm

from jinja2 import Environment, FileSystemLoader

from owl.data import common
from owl.data import img_tools
from owl.data import dim_reductor
from owl.data import mongo_manager
from owl.features import obj_feat_extractor
from owl.search import common as search_common
from owl.search import simple_matchers


class VisualSearchPipeline(object):
  """Pipeline for visual search.

  Used for local development to evaluate feature and matching performance.

  1) read in files and organize into database and query.
  2) compute features and save to database: [img_fn, label, type, feat1, feat2, ...].
  3) reduce feature dimension if too high (x00~1000+) and save to database.
  4) run matching.
  5) evalute.
  All db involved: [task_name]_db.raw_feats, [task_name]_db.compressed_feats,
                   [task_name]_query.raw_feats, [task_name]_query.compressed_feats.
  """

  res_dir = None
  # list of tuple for items.
  db_items = []
  query_items = []
  # each feature type is a numpy array.
  db_feats = {}
  query_feats = {}
  ranked_lists = None
  logger = None
  item_db = None
  raw_feat_db = None
  compressed_feat_db = None
  # task statistics.
  res_info = {}
  save_data_fn = ""
  task_name = ""
  task_db_db_name = ""
  task_query_db_name = ""
  target_feat_name = ""

  def __init__(self, task_name, res_dir):
    self.task_name = task_name
    self.task_db_db_name = "{}_db".format(self.task_name)
    self.task_query_db_name = "{}_query".format(self.task_name)
    self.item_db = mongo_manager.MongoManager()
    self.raw_feat_db = mongo_manager.MongoManager()
    self.compressed_feat_db = mongo_manager.MongoManager()
    self.res_dir = res_dir
    log_fn = os.path.join(res_dir, "log.txt")
    self.logger = common.get_logger("visualsearchlogger", log_fn)

  def clean_db(self):
    """Remove all related database.
    """
    self.item_db.connect(db_name=self.task_db_db_name)
    self.item_db.delete_db(self.task_db_db_name)
    self.item_db.delete_db(self.task_query_db_name)

  def load_items_from_db(self):
    """Load data from local db.
    """
    # load db items.
    self.db_items = []
    self.item_db.connect(db_name=self.task_db_db_name, collection_name="items")
    db_cursor = self.item_db.get_scan_cursor()
    for db_item in db_cursor:
      self.db_items.append(db_item)
    print "{} db items loaded from db.".format(len(self.db_items))
    # load query items.
    self.query_items = []
    self.item_db.switch_db_collection(self.task_query_db_name, "items")
    query_cursor = self.item_db.get_scan_cursor()
    for query_item in query_cursor:
      self.query_items.append(query_item)
    print "{} query items loaded from db.".format(len(self.query_items))
    self.item_db.disconnect()

  def load_feats_from_db(self):
    """Load features from db.

    At the same time, load item with the same order.
    """
    # load db data.
    self.item_db.connect(db_name=self.task_db_db_name, collection_name="items")
    self.compressed_feat_db.connect(
        db_name=self.task_db_db_name, collection_name="compressed_feats")
    self.db_feats = None
    self.db_items = []
    db_cursor = self.compressed_feat_db.get_scan_cursor()
    total_item_count = db_cursor.count()
    for db_id, db_feat_item in enumerate(db_cursor):
      db_item_id = db_feat_item["_id"]
      db_feat = np.array(db_feat_item[self.target_feat_name]).reshape(1, -1)
      if self.db_feats is None:
        self.db_feats = {}
        self.db_feats[self.target_feat_name] = np.zeros(
            (total_item_count, db_feat.shape[1]))
      self.db_feats[self.target_feat_name][db_id] = db_feat
      cur_item = self.item_db.query(value_list=[db_item_id])[0]
      self.db_items.append(cur_item)
      if len(self.db_items) % 1000 == 0:
        print "loaded {}/{} items".format(len(self.db_items), total_item_count)

    # load query data.
    self.item_db.connect(
        db_name=self.task_query_db_name, collection_name="items")
    self.compressed_feat_db.connect(
        db_name=self.task_query_db_name, collection_name="compressed_feats")
    self.query_feats = None
    self.query_items = []
    item_cursor = self.compressed_feat_db.get_scan_cursor()
    total_item_count = item_cursor.count()
    for feat_id, feat_item in enumerate(item_cursor):
      item_id = feat_item["_id"]
      feat = np.array(feat_item[self.target_feat_name]).reshape(1, -1)
      if self.query_feats is None:
        self.query_feats = {}
        self.query_feats[self.target_feat_name] = np.zeros(
            (total_item_count, feat.shape[1]))
      self.query_feats[self.target_feat_name][feat_id] = feat
      cur_item = self.item_db.query(value_list=[item_id])[0]
      self.query_items.append(cur_item)
      if len(self.query_items) % 1000 == 0:
        print "loaded {}/{} items".format(
            len(self.query_items), total_item_count)
    self.item_db.disconnect()
    self.compressed_feat_db.disconnect()

  def read_data_from_files(self, img_folder, img_exts):
    """Input image data.

    Args:
      img_folder: folder contains image files.
    If has subfolders, each is treated as a category with folder name.
    """
    # read all image files.
    img_fns, img_labels, _ = common.list_img_files(img_folder, img_exts)
    # split into query and database.
    db_ids, _, query_ids = common.split_train_val_test(
        img_labels, train_ratio=0.8, test_ratio=0.2)
    self.logger.info("{} db files and {} query files found.".format(
        len(db_ids), len(query_ids)))
    # save db item info.
    self.item_db.connect(db_name=self.task_db_db_name, collection_name="items")
    self.item_db.delete_collection()
    for i, db_id in enumerate(db_ids):
      cur_db_item = {"img_fn": img_fns[db_id], "label": img_labels[db_id]}
      self.item_db.add(cur_db_item)
      if i % 100 == 0:
        self.logger.info("{}/{} db items added.".format(i, len(db_ids)))
    self.logger.info("all db items added to db.")
    # save query item info.
    self.item_db.switch_db_collection(self.task_query_db_name, "items")
    self.item_db.delete_collection()
    for i, query_id in enumerate(query_ids):
      cur_query_item = {
          "img_fn": img_fns[query_id],
          "label": img_labels[query_id]
      }
      self.item_db.add(cur_query_item)
      if i % 100 == 0:
        self.logger.info("{}/{} query items added.".format(i, len(query_ids)))
    self.logger.info("all query items added to db.")
    self.item_db.disconnect()

  def compute_feats(self, features, batch_size=10):
    """Compute features for all images.

    Args:
      features: feature extractors.
      batch_size: image batch to process.
    """
    # set up feature extractors.
    self.logger.info("start feature extraction...")
    feat_extractor = obj_feat_extractor.GenericObjFeatExtractor(
        features=features)
    startt = time.time()
    feat_extractor.start()
    self.logger.info("feature extractor start time: {}s".format(time.time() -
                                                                startt))
    # compute features for db.
    self.raw_feat_db.connect(
        db_name=self.task_db_db_name, collection_name="raw_feats")
    self.raw_feat_db.delete_collection()
    startt = time.time()
    self.db_feats = {}
    for idx in range(0, len(self.db_items), batch_size):
      try:
        batch_items = self.db_items[idx:idx + batch_size]
        rgb_imgs = []
        # group images.
        for item in batch_items:
          img_bin = img_tools.read_img_bin(item["img_fn"])
          img_arr = img_tools.img_bin_to_numpy_rgb(img_bin)
          rgb_imgs.append(img_arr)
        # compute batch features.
        startt2 = time.time()
        cur_feats = feat_extractor.compute_batch(rgb_imgs)
        self.logger.info("batch feature extraction time: {}s".format(time.time(
        ) - startt2))
        # save feature to database.
        batch_feat_objs = []
        for item_id, item in enumerate(batch_items):
          cur_feat_obj = {}
          cur_feat_obj["_id"] = item["_id"]
          for feat_name, batch_feats in cur_feats.iteritems():
            cur_feat_obj[feat_name] = batch_feats[item_id].tolist()
          batch_feat_objs.append(cur_feat_obj)
        self.raw_feat_db.add_many(batch_feat_objs)
        self.logger.info("database feature: {}/{}".format(
            min(idx + batch_size, len(self.db_items)), len(self.db_items)))
      except Exception as ex:
        self.logger.error("{}, skip one batch".format(ex.message))
        continue

    self.logger.info("database feature extraction done. time cost: {}s".format(
        time.time() - startt))

    # compute features for query.
    self.raw_feat_db.switch_db_collection("{}_query".format(self.task_name),
                                          "raw_feats")
    self.raw_feat_db.delete_collection()
    startt = time.time()
    self.query_feats = {}
    for idx in range(0, len(self.query_items), batch_size):
      try:
        rgb_imgs = []
        batch_items = self.query_items[idx:idx + batch_size]
        for item in batch_items:
          img_bin = img_tools.read_img_bin(item["img_fn"])
          img_arr = img_tools.img_bin_to_numpy_rgb(img_bin)
          rgb_imgs.append(img_arr)
        startt2 = time.time()
        cur_feats = feat_extractor.compute_batch(rgb_imgs)
        self.logger.info("batch feature extraction time: {}s".format(time.time(
        ) - startt2))
        # save feature to database.
        batch_feat_objs = []
        for item_id, item in enumerate(batch_items):
          cur_feat_obj = {}
          cur_feat_obj["_id"] = item["_id"]
          for feat_name, batch_feats in cur_feats.iteritems():
            cur_feat_obj[feat_name] = batch_feats[item_id].tolist()
          batch_feat_objs.append(cur_feat_obj)
        self.raw_feat_db.add_many(batch_feat_objs)
        self.logger.info("query feature: {}/{}".format(
            min(idx + batch_size, len(self.query_items)),
            len(self.query_items)))
      except Exception as ex:
        self.logger.error("{}, skip one batch".format(ex.message))
        continue

    self.logger.info("query feature extraction done. time cost: {}s".format(
        time.time() - startt))
    self.raw_feat_db.disconnect()

  def compress_feats(self, train_compressor=True):
    """Compress features.
    """
    batch_size = 200
    reducer = dim_reductor.IncrementalPCADimReducer(
        self.res_dir, 128, batch_size=batch_size)
    self.raw_feat_db.connect(
        db_name=self.task_db_db_name, collection_name="raw_feats")
    if train_compressor:
      db_item_cursor = self.raw_feat_db.get_scan_cursor()
      total_db_item_count = db_item_cursor.count()
      print "total db item to compress: {}".format(total_db_item_count)
      db_raw_feats_batch = None
      batch_item_count = 0
      total_item_count = 0
      for db_item in db_item_cursor:
        cur_feat = np.array(db_item[self.target_feat_name])
        cur_feat = cur_feat.reshape(1, -1)
        batch_item_count += 1
        total_item_count += 1
        if db_raw_feats_batch is None:
          db_raw_feats_batch = cur_feat
        else:
          db_raw_feats_batch = np.vstack((db_raw_feats_batch, cur_feat))
        if batch_item_count >= batch_size:
          print "{}/{} db features loaded.".format(total_item_count,
                                                   total_db_item_count)
          print db_raw_feats_batch.shape
          reducer.train(db_raw_feats_batch, False)
          print "dim reducer updated."
          db_raw_feats_batch = None
          batch_item_count = 0
    else:
      reducer.save_load_model(to_save=False)

    def _compress_feats(db_type):
      """Actually compress feats in a db.

      Args:
        db_type: "db" or "query".
      """
      if db_type == "db":
        self.logger.info("start compressing db features")
        self.raw_feat_db.connect(
            db_name=self.task_db_db_name, collection_name="raw_feats")
        self.compressed_feat_db.connect(
            db_name=self.task_db_db_name, collection_name="compressed_feats")
      else:
        self.logger.info("start compressing query features")
        self.raw_feat_db.connect(
            db_name=self.task_query_db_name, collection_name="raw_feats")
        self.compressed_feat_db.connect(
            db_name=self.task_query_db_name,
            collection_name="compressed_feats")
      self.compressed_feat_db.delete_collection()
      # compress raw feats.
      if db_type == "db":
        self.db_feats = {}
      else:
        self.query_feats = {}
      raw_item_cursor = self.raw_feat_db.get_scan_cursor()
      db_item_count = raw_item_cursor.count()
      batch_item_count = 0
      processed_item_count = 0
      batch_feats = None
      batch_objs = []
      for item in raw_item_cursor:
        batch_item_count += 1
        processed_item_count += 1
        old_feat = np.array(item[self.target_feat_name]).reshape(1, -1)
        if batch_feats is None:
          batch_feats = old_feat
        else:
          batch_feats = np.vstack((batch_feats, old_feat))
        cur_obj = {"_id": item["_id"]}
        batch_objs.append(cur_obj)
        if batch_item_count >= batch_size:
          new_feats = reducer.transform(batch_feats)
          # add to class feats for matching.
          if db_type == "db":
            if self.target_feat_name not in self.db_feats:
              self.db_feats[self.target_feat_name] = new_feats
            else:
              self.db_feats[self.target_feat_name] = np.vstack(
                  (self.db_feats[self.target_feat_name], new_feats))
          else:
            if self.target_feat_name not in self.query_feats:
              self.query_feats[self.target_feat_name] = new_feats
            else:
              self.query_feats[self.target_feat_name] = np.vstack(
                  (self.query_feats[self.target_feat_name], new_feats))
          for idx, new_feat in enumerate(new_feats):
            batch_objs[idx][self.target_feat_name] = new_feat.tolist()
          # add to database.
          self.compressed_feat_db.add_many(batch_objs)
          self.logger.info("{}/{} compressed feature added to db.".format(
              processed_item_count, db_item_count))
          # clean.
          batch_item_count = 0
          batch_objs = []
          batch_feats = None
      self.logger.info("feature compression done.")

    # compress features.
    _compress_feats("db")
    _compress_feats("query")

    # clean.
    self.raw_feat_db.disconnect()
    self.compressed_feat_db.disconnect()

  def run_match(self, protocol):
    """Perform matching between query and database.
    """
    self.logger.info("start matching...")
    if protocol == search_common.MatchProtocol.EXACT:
      matcher = simple_matchers.ExactMatcher(
          "matcher", search_common.MatcherType.L2, self.res_dir)
    else:
      matcher = simple_matchers.ANNMatcher(
          "matcher", search_common.MatcherType.L2, 128, self.res_dir)
    # set database.
    if len(self.db_feats) == 0 or len(self.query_feats) == 0:
      self.load_feats_from_db()
    assert len(self.db_feats) > 0 and len(self.query_feats) > 0, \
      "db or query feature is empty"
    db_items = {"metadata": []}
    db_items["features"] = self.db_feats.values()[0]
    matcher.prepare_database(db_items)
    query_items = {"metadata": []}
    query_items["features"] = self.query_feats.values()[0]
    startt = time.time()
    self.ranked_lists = matcher.match(query_items, top_nn=20)
    self.logger.info("match time: {}s".format(time.time() - startt))
    self.logger.info("matching done.")

  def evaluate(self, res_dir):
    """Compute retrieval accuracy and visualize results.

    Args:
      res_dir: directory to put result data.
    """
    # get result display name from save directory.
    res_name = res_dir.rstrip("/")
    res_name = os.path.basename(res_name)
    self.logger.info("start evaluation...")
    # compute accuracy: top1, top5, top10, top20.
    accu_rank = [1, 5, 10, 20]
    top_k_accu = [0, 0, 0, 0]
    # for each query.
    for query_id, cur_ranked_ids in enumerate(self.ranked_lists):
      for k, rank in enumerate(accu_rank):
        top_k_accu[k] += np.mean([
            1
            if self.query_items[query_id]["label"] == self.db_items[x]["label"]
            else 0 for x in cur_ranked_ids[:rank]
        ])
    top_k_accu = [x / len(self.query_items) for x in top_k_accu]
    # visualize results.
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(cur_dir), trim_blocks=True)
    # prepare ranked list filenames: [query, db_list].
    db_ranked_fns = []
    db_ranked_labels = []
    for cur_ranked_ids in self.ranked_lists:
      db_ranked_fns.append(
          [self.db_items[x]["img_fn"] for x in cur_ranked_ids[:10]])
      db_ranked_labels.append(
          [self.db_items[x]["label"] for x in cur_ranked_ids[:10]])
    # render webpage.
    query_files = [x["img_fn"] for x in self.query_items]
    query_labels = [x["label"] for x in self.query_items]
    res_str = j2_env.get_template("match_vis_temp.html").render(
        test_name=res_name,
        query_fns=query_files[:100],
        query_labels=query_labels[:100],
        db_fns=db_ranked_fns[:100],
        db_labels=db_ranked_labels[:100],
        rank_accu=zip(accu_rank, top_k_accu))
    res_fn = os.path.join(res_dir, "match_vis.html")
    with open(res_fn, "w") as fn:
      fn.write(res_str)
      self.logger.info("results saved to {}".format(res_fn))

  def run(self,
          img_folder,
          img_exts,
          features,
          batch_size,
          match_protocol,
          load_items_from_db=False,
          compute_feats=False,
          compress_feats=False):
    """All in one method to run pipeline.

    Be able to use the same data split with different
    features for comparison.
    """
    self.target_feat_name = features[0].feat_name
    if load_items_from_db:
      self.load_items_from_db()
    else:
      self.read_data_from_files(img_folder, img_exts)
      self.load_items_from_db()
    if compute_feats:
      self.compute_feats(features, batch_size)
    if compress_feats:
      self.compress_feats(train_compressor=False)
    self.run_match(match_protocol)
    self.evaluate(self.res_dir)
