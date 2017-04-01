"""Cifar10 example using DeepModels.
"""

import os
import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from ...core import commons
from ...core.tf import common_flags
from ...core.tf import base_model
from ...core.tf import model_zoo
from ...core.tf import losses as dm_losses
from ...tools import data_manager

tf.logging.set_verbosity(tf.logging.INFO)

flags = tf.app.flags
FLAGS = flags.FLAGS


def run_cifar10(is_training=True):
  if is_training:
    # prepare training data input.
    batch_size = FLAGS.batch_size
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(cur_dir, "../../", "data/cifar-10-python/")
    train_data, train_labels, _, _ = data_manager.load_cifar10(data_dir)
    # switch dimension.
    train_data = np.transpose(train_data, (0, 2, 3, 1))
    img_tensor = tf.convert_to_tensor(train_data, tf.float32)
    label_tensor = tf.convert_to_tensor(train_labels, tf.int64)
    img_batch, label_batch = tf.train.shuffle_batch(
        [img_tensor, label_tensor],
        batch_size=batch_size,
        enqueue_many=True,
        capacity=batch_size * 100,
        min_after_dequeue=batch_size * 50)
    print img_batch.get_shape()
    print label_batch.get_shape()
    # build model.
    net_outputs, _ = model_zoo.build_net(commons.NetNames.CIFAR10, img_batch,
                                         10)
    base_model.print_variable_names()
    # compute loss.
    clf_loss = dm_losses.clf_loss(net_outputs, label_batch)
    # train.
    train_test_params = commons.TrainTestParams(FLAGS.log_dir)
    base_model.train_model_given_loss(clf_loss, None, train_test_params)
  else:
    pass


def main(_):
  run_cifar10()


if __name__ == "__main__":
  tf.app.run()