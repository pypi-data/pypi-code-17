"""Build a image classifier in DeepModels.

Show how to create an all-in-one deep model class with
existing building blocks.
1) train from stratch.
2) fine-tune a model.
3) evaluate model.

usage: train model, test model, launch tensorboard
"""

import copy

import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.python import pywrap_tensorflow

from deepmodels.core import commons
from deepmodels.core.tf import common_flags
from deepmodels.core.tf import base_model
from deepmodels.core.tf import data_provider
from deepmodels.core.tf import model_zoo
from deepmodels.core.tf.templates.dm_classifier import DMClassifier

tf.logging.set_verbosity(tf.logging.INFO)

flags = tf.app.flags
FLAGS = flags.FLAGS


def tf_print_var(target_var, msg):
  target_var = tf.Print(target_var, [target_var], message=msg, summarize=10)
  return target_var


class MyImgClassifer(DMClassifier):
  """A example class of classifier.
  """
  train_net_type = commons.NetNames.INCEPTION_V3
  pred_net_type = commons.NetNames.INCEPTION_V3

  def build_model(self, inputs, model_params):
    """Create a model to be trained from stratch.
    """
    net, endpoints = model_zoo.build_net(
        self.train_net_type,
        inputs,
        model_params.cls_num,
        mode=model_params.model_mode)
    return net, endpoints

  def simple_ft_model(self, inputs, model_params):
    """Simple one layer classifier.

    Assume inputs are features already.
    """
    with tf.variable_scope("simple_ft"):
      with slim.arg_scope(
          [slim.fully_connected],
          weights_initializer=tf.truncated_normal_initializer(stddev=0.001)):
        net = slim.fully_connected(
            inputs, model_params.cls_num, activation_fn=None, scope="logits")
    return net

  def compute_losses(self, gt_labels, pred_logits, endpoints):
    """Custom loss definition.
    """
    if 'AuxLogits' in endpoints:
      print "aux loss included."
      aux_loss = slim.losses.softmax_cross_entropy(
          endpoints['AuxLogits'], gt_labels, weight=0.4, scope='aux_loss')
      tf.scalar_summary("losses/aux_loss", aux_loss)
    clf_loss = slim.losses.softmax_cross_entropy(
        pred_logits, gt_labels, weight=1.0, scope="clf_loss")
    tf.scalar_summary("losses/clf_loss", clf_loss)

  def simple_finetune(self, train_img_batch, train_label_batch, model_params,
                      train_params):
    """Extract features first and ft linear model.
    """
    net_params = model_zoo.net_params[self.train_net_type]
    tmp_model_params = copy.deepcopy(model_params)
    tmp_model_params.model_mode = commons.ModelMode.TEST
    tmp_model_params.cls_num = net_params.cls_num
    _, end_points = self.build_model(train_img_batch, tmp_model_params)
    self.vars_to_restore = slim.get_variables()
    feats = end_points["feats"]
    feats = tf.squeeze(feats)
    max_feat = tf.reduce_max(feats)
    max_pixel = tf.reduce_max(train_img_batch)
    pred_logits = self.simple_ft_model(feats, model_params)
    self.vars_to_train = slim.get_variables(scope="simple_ft")
    labels = slim.one_hot_encoding(train_label_batch, model_params.cls_num)
    # pred_logits = tf.Print(pred_logits, [max_feat, max_weights, max_bias, max_pixel], message="max feat, max weight, max bias, max pixel")
    # pred_logits = tf_print_var(pred_logits, "logits")
    # labels = tf_print_var(labels, "labels")
    clf_loss = slim.losses.softmax_cross_entropy(
        pred_logits, labels, scope="clf_loss")
    tf.scalar_summary("losses/clf_loss", clf_loss)
    model_fn = model_zoo.get_default_net_weights_fn(self.train_net_type)
    init_fn = slim.assign_from_checkpoint_fn(model_fn, self.vars_to_restore)
    base_model.print_variable_names(self.vars_to_train, "to train")
    base_model.train_model_given_loss(
        slim.losses.get_total_loss(),
        self.vars_to_train,
        train_params,
        init_fn=init_fn)

  def test_simple_finetune(self, test_img_batch, test_label_batch,
                           model_params, test_params):
    net_params = model_zoo.net_params[self.train_net_type]
    tmp_model_params = copy.deepcopy(model_params)
    tmp_model_params.model_mode = commons.ModelMode.TEST
    tmp_model_params.cls_num = net_params.cls_num
    _, end_points = self.build_model(test_img_batch, tmp_model_params)
    feats = end_points["feats"]
    feats = tf.squeeze(feats)
    pred_logits = self.simple_ft_model(feats, model_params)
    pred_cls = tf.argmax(pred_logits, 1)
    metric_args = {
        "eval/mean_clf_accuracy":
        slim.metrics.streaming_accuracy(pred_cls, test_label_batch)
    }
    base_model.test_model_given_metrics(metric_args, test_params)


def main(_):
  # create object.
  clf = MyImgClassifer()
  model_params = commons.ModelParams("demo_clf")

  if FLAGS.task in {0, 1, 2, 3}:
    clf.train_net_type = commons.NetNames.INCEPTION_V3
    net_params = model_zoo.net_params[clf.train_net_type]
    if FLAGS.task in {0, 1}:
      model_params.model_mode = commons.ModelMode.TRAIN
    else:
      model_params.model_mode = commons.ModelMode.TEST
    if FLAGS.task in {1, 3}:
      preprocess_fn = model_zoo.net_preprocess(
          clf.train_net_type, model_mode=model_params.model_mode)
    else:
      preprocess_fn = None

    batch_data = data_provider.clf_input_from_image_fns(
        FLAGS.input_meta,
        3,
        net_params.input_img_width,
        net_params.input_img_height,
        FLAGS.batch_size,
        scaling=True,
        preprocess_fn=preprocess_fn,
        shuffle=True)
    img_batch, label_batch, _, samp_num, cls_num = batch_data
    tf.image_summary("input image", img_batch, 3)
    print "image batch shape: {}".format(img_batch.get_shape())
    print "label batch shape: {}".format(label_batch.get_shape())
    print "total sample number: {}; class number: {}".format(samp_num, cls_num)
    model_params.cls_num = cls_num
    if FLAGS.task in {0, 1}:
      train_test_params = commons.TrainTestParams(
          log_dir=FLAGS.log_dir,
          batch_size=FLAGS.batch_size,
          samp_num=samp_num,
          max_epochs=15)
      train_test_params.init_learning_rate = 0.001
      train_test_params.opt_method = commons.OPTMethod.SGD
      train_test_params.save_summaries_secs = 60
      train_test_params.save_interval_secs = 60
      if FLAGS.task == 0:
        train_test_params.resume_training = True
        model_params.custom[
            "train_scopes"] = ["InceptionV3/Logits", "InceptionV3/AuxLogits"]
        clf.train(img_batch, label_batch, model_params, train_test_params)
      else:
        if clf.train_net_type == commons.NetNames.INCEPTION_V3:
          model_params.custom["restore_scopes_exclude"] = [
              "InceptionV3/Logits", "InceptionV3/AuxLogits"
          ]
          model_params.custom["train_scopes"] = [
              "InceptionV3/Logits", "InceptionV3/AuxLogits"
          ]
        if clf.train_net_type == commons.NetNames.VGG16:
          model_params.custom["restore_scopes_exclude"] = ["vgg_16/fc8"]
          model_params.custom["train_scopes"] = ["vgg_16/fc8"]
        # clf.simple_finetune(img_batch, label_batch, model_params, train_test_params)
        clf.train(img_batch, label_batch, model_params, train_test_params)
    else:
      train_test_params = commons.TrainTestParams(
          log_dir=FLAGS.log_dir,
          batch_size=FLAGS.batch_size,
          samp_num=samp_num,
          max_epochs=FLAGS.test_ratio)
      train_test_params.save_summaries_secs = 60
      train_test_params.eval_secs = 100
      model_params.custom["test_ft"] = True if FLAGS.task == 3 else False
      if clf.train_net_type == commons.NetNames.INCEPTION_V3:
        # clf.test_simple_finetune(img_batch, label_batch, model_params, train_test_params)
        clf.test(img_batch, label_batch, model_params, train_test_params)

  if FLAGS.task == 4:
    test_model_restore()


if __name__ == "__main__":
  tf.app.run()
