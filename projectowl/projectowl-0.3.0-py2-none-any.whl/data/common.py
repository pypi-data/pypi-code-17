"""Shared code for data.
"""

import datetime
import glob
import logging
import os
import random


def append_url_params(base_url, param_dict):
  """Append parameters to a base url.

  Args:
    base_url: the basic url, end with ?
    param_dict: dictionary of parameters.
  Returns:
    a complete url.
  """
  url = base_url
  # indicate if a parameter is attached.
  started = False
  for key, val in param_dict.iteritems():
    if val is not None:
      url = url + "&" if started else url
      url += "{}={}".format(key, val)
      started = True
  return url


def split_train_val_test(labels,
                         train_ratio=0.7,
                         val_ratio=0.0,
                         test_ratio=0.3):
  """split a dataset into train, val and test subsets.

  The split is balanced across classes.

  Args:
    labels: a list of label ids.
    train_ratio: percentage of samples for training.
    val_ratio: percentage of samples for validation.
    test_ratio: percentage of samples for test.
  Returns:
    list of sample ids for train, val, test sets.
  """
  assert (train_ratio + val_ratio + test_ratio == 1
          ), "percentages must add up to 1"
  train_ids = []
  val_ids = []
  test_ids = []
  # split for each class evenly.
  unique_labels = set(labels)
  for label in unique_labels:
    indices = [i for i, v in enumerate(labels) if v == label]
    num = len(indices)
    train_num = int(num * train_ratio)
    val_num = int(num * val_ratio)
    random.shuffle(indices)
    train_ids += indices[:train_num]
    val_ids += indices[train_num:train_num + val_num]
    test_ids += indices[train_num + val_num:]
  return train_ids, val_ids, test_ids


def list_img_files(img_root_dir, img_exts=None, has_cate_subfolder=True):
  """Get image file names from a folder.

  Supported image file format: jpg, jpeg, png, bmp.

  Args:
    img_root_dir: root directory of image files.
    img_exts: target image extensions, e.g. [*.png, *.jpg].
    has_cate_subfolder: whether root contains subfolders for categories.
  Returns:
    image file names and labels if category exists.
  """
  img_fns = []
  all_exts = ["*.png", "*.jpg", "*.jpeg", "*.bmp"]
  if img_exts is None:
    img_exts = all_exts
  else:
    for img_ext in img_exts:
      assert img_ext in all_exts, "{} file type not supported".format(img_ext)
  if has_cate_subfolder:
    cate_dirs = os.listdir(img_root_dir)
    cate_dirs = [os.path.join(img_root_dir, x) for x in cate_dirs]
    cate_dirs = [x for x in cate_dirs if os.path.isdir(x)]
    img_labels = []
    label_names = {}
    for cate_id, cur_cate_dir in enumerate(cate_dirs):
      cur_cate_name = os.path.basename(cur_cate_dir.strip("/"))
      label_names[cate_id] = cur_cate_name
      # find all image files.
      all_img_fns = []
      for img_ext in img_exts:
        cur_ext_fns = glob.glob(os.path.join(cur_cate_dir, img_ext))
        all_img_fns += cur_ext_fns
      img_labels += [cate_id] * len(all_img_fns)
      img_fns += all_img_fns
    return img_fns, img_labels, label_names
  else:
    for img_ext in img_exts:
      cur_ext_fns = glob.glob(os.path.join(cur_cate_dir, img_ext))
      img_fns += cur_ext_fns
    return img_fns


def get_logger(name, log_fn):
  """Get a logger that outputs to log_fn and stdout.

  Args:
    name: name of the logger.
    log_fn: file to save log data.
  Returns:
    a logger object. use as logger.info, logger.error.
  """
  logger = logging.getLogger(name)
  logger.setLevel(logging.INFO)
  logger.addHandler(logging.StreamHandler())
  fh = logging.FileHandler(log_fn)
  logger.addHandler(fh)
  return logger


def get_datenow_str():
  """Get a properly formatted string for current date and time.
  """
  now = datetime.datetime.now()
  now_str = now.strftime("%Y_%b_%d_%H_%M_%S")
  return now_str
