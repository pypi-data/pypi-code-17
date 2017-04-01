"""Database management for web api.

NOTE: for linux dev, use mongobooster to inspect database content visually.
"""

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


def objectid_to_str(object_id):
  return str(object_id)


def str_to_objectid(id_str):
  return ObjectId(id_str)


class MongoManager(object):
  """MongoDB manager.
  """

  # data
  client = None
  db = None
  collection = None

  def __init__(self):
    pass

  def is_connection_valid(self):
    """Check if connection is valid.
    """
    if self.client == None or \
    self.db == None or \
    self.collection == None:
      print "db connection invalid"
      return False
    else:
      return True

  def connect(self,
              user=None,
              pwd=None,
              host=None,
              port=None,
              db_name=None,
              collection_name=None):
    """Connect to mongodb server.

    Args:
      user: user to login.
      pwd: pwd to login.
      host: server host.
      port: port to use.
      db_name: database to use.
      collection_name: collection to use.
    """
    # make url.
    db_url = "mongodb://"
    if user is not None:
      db_url += user
    if pwd is not None:
      db_url += ":{}@".format(pwd)
    db_url += host if host is not None else "127.0.0.1"
    db_url += ":{}".format(port) if port is not None else ":27017"
    # get client.
    print "connecting to mongodb: {}".format(db_url)
    self.client = MongoClient(db_url)
    if db_name is not None:
      self.db = self.client[db_name]
      print "use db: {}".format(db_name)
    else:
      self.db = self.client["test"]
    if collection_name is not None:
      self.collection = self.db[collection_name]
      print "use collection: {}".format(collection_name)
    else:
      self.collection = self.db["test"]
    print "mongodb connected"

  def delete_db(self, db_name):
    """Delete database.
    """
    self.client.drop_database(db_name)
    print "removed db: {}".format(db_name)

  def delete_collection(self):
    """delete collection for current db.
    """
    self.collection.drop()
    print "current collection dropped."

  def switch_db_collection(self, db_name, collection_name):
    """Select a specific collection.
    """
    assert self.client is not None, "db is not connected."
    self.db = self.client[db_name]
    self.collection = self.db[collection_name]
    print "db switch to: {}.{}".format(db_name, collection_name)

  def disconnect(self):
    """disconnect from server.
    """
    if self.client is not None:
      self.client.close()

  def add(self, obj):
    """Add a new document.

    Args:
      obj: document to insert.
    Returns:
      object_id of the inserted document.
    """
    self.collection.insert_one(obj)

  def add_many(self, obj_list):
    """Add a list of objects together.

    Args:
      obj_list: documents to insert.
    """
    self.collection.insert_many(obj_list)

  def get_scan_cursor(self):
    """Return cursor to all documents.
    """
    cursor = self.collection.find()
    return cursor

  def query(self, attribute="_id", value_list=None):
    """query a set of objects using certain attribute.

    Args:
      attribute: name of the attribute.
      value_list: list of values to search for the attribute.
    Returns:
      found objects.
    """
    if not self.is_connection_valid():
      return
    res = []
    for val in value_list:
      doc = self.collection.find_one({attribute: val})
      res.append(doc)
    return res

  def update(self, obj_id, new_key_vals):
    """Update an object.

    Args:
      obj_id: object id object.
      new_key_vals: dict of new key value pairs.
    """
    try:
      update_res = self.collection.update_one({
          "_id": obj_id
      }, {"$set": new_key_vals})
    except pymongo.errors.PyMongoError as ex:
      print "error {}".format(ex)

  def PopulateDB(self):
    print 'start populating database'

    # connect db
    db_man = MongoManager()
    db_man.load_config(self.config_fn)
    db_man.connect()
    print 'database connected'

    # compute for each item
    total_cnt = db_man.collection.count()
    print 'total object to process: {}'.format(total_cnt)
    valid_num = 0
    cursor = db_man.collection.find()
    for item in cursor:
      try:
        img_fn = item['img_file_path']
        mask_fn = item['mask_file_path']
        cur_feats = self.Compute(img_fn, mask_fn)
        # update each feature
        for feat_name, feat_val in cur_feats.iteritems():
          db_man.update({
              '_id': item['_id']
          }, 'visual_features.' + feat_name, feat_val)
        valid_num += 1
        if valid_num % 1000 == 0:
          print 'finished {}/{}'.format(valid_num, total_cnt)
      except Exception as ex:
        print 'error in {}: {}'.format(img_fn, ex.message)
        continue

    print 'feature extraction done. {}/{} finished. Percentage: {}%'.format(
        valid_num, total_cnt, valid_num * 100.0 / total_cnt)


if __name__ == '__main__':
  dm = MongoManager()
  config_fn = 'E:/Projects/Github/VisualSearchEngine/Owl/Settings/engine_settings2.json'
  dm.load_config(config_fn)
