"""Tests for DeepModels data.
"""

import os
import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from ... import commons
from .. import data_provider
from .. import model_zoo

tf.logging.set_verbosity(tf.logging.INFO)


class TFDataTest(tf.test.TestCase):
  """Test dm data related stuff.
  """

  def test_img_metadata_gen(self):
    img_dir = "/Users/jiefeng/dev/data/101_ObjectCategories/"
    save_fn_prefix = "/Users/jiefeng/dev/data/random_test/caltech101"
    data_provider.gen_clf_metadata_from_img_fns(img_dir, save_fn_prefix)
    train_fn = save_fn_prefix + "__train.csv"
    test_fn = save_fn_prefix + "__test.csv"
    self.assertTrue(os.path.exists(train_fn))
    self.assertTrue(os.path.exists(test_fn))

  def test_img_fn_input(self):
    """Test batch image input.
    """
    # meta_fn = "/mnt/DataHouse/Fashion/EyeStyle/deepmodels_tf_data/eyestyle_092416__test.csv"
    meta_fn = "/home/jiefeng/datasets/fashion/dm_data/eyestyle__test.csv"
    batch_size = 12
    batch_data = data_provider.clf_input_from_image_fns(
        meta_fn, 3, 224, 224, batch_size, shuffle=True)
    img_batch, label_batch, fn_batch, _, _ = batch_data
    max_pixel_val = tf.reduce_max(img_batch)
    min_pixel_val = tf.reduce_min(img_batch)
    max_label_val = tf.reduce_max(label_batch)
    min_label_val = tf.reduce_min(label_batch)
    with self.test_session() as sess:
      sess.run(tf.initialize_all_variables())
      coord = tf.train.Coordinator()
      threads = tf.train.start_queue_runners(coord=coord)
      for i in range(20):
        print "batch {}:".format(i)
        cur_fn, cur_label = sess.run([fn_batch, label_batch])
        print cur_fn
        print cur_label
        print "max/min pixel values: {} {}".format(max_pixel_val.eval(),
                                                   min_pixel_val.eval())
        print "max/min label values: {} {}".format(max_label_val.eval(),
                                                   min_label_val.eval())
      coord.request_stop()
      coord.join(threads)

  def test_dataset_labels(self):
    label_names_dict = model_zoo.net_label_names(commons.NetNames.INCEPTION_V3)
    self.assertEqual(len(label_names_dict.keys()), 1001)
    label_names_dict = model_zoo.net_label_names(commons.NetNames.VGG16)
    self.assertEqual(len(label_names_dict.keys()), 1000)


if __name__ == "__main__":
  tf.test.main()