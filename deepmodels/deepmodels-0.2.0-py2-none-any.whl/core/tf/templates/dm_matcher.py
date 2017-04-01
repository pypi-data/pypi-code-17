"""Template class for image matcher.
"""

import os
import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from ... import commons
from .. import base_model
from .. import common_flags
from .. import losses
from ....tools import data_manager
from ....tools import search_tools

flags = tf.app.flags
FLAGS = flags.FLAGS


class DMMatcher(object):
  """A template class of matcher using triplet loss.

  Work with general feature input or image feature.

  Attributes:
    input_tensor_name: name of input tensor.
    output_tensor_name: name of output tensor.
    vars_to_train: variables to train.
    vars_to_restore: variables to restore from a model file.
    sess: tf.Session object to perserve a session for constant prediction.
  """
  input_tensor_name = "inputs"
  output_tensor_name = "outputs"
  vars_to_train = None
  vars_to_restore = None
  sess = None

  def __init__(self):
    self.sess = tf.Session()

  def __del__(self):
    if self.sess is not None:
      self.sess.close()

  def build_model(self, inputs, model_params):
    """Construct deep model.

    Override to define a custom model.
    Compute feature embedding for inputs.

    Args:
      inputs: input data, either data vectors or images.
    Stacks of triplet batches.
      model_params: model related parameters.
    Returns:
      feature and endpoints.
    """
    pass

  def set_key_vars(self, restore_scope_exclude, train_scopes):
    """Set vars_to_train and vars_to_restore.

    Called after build_model.

    Args:
      restore_scope_exclude: variable scopes to exclude for restoring.
      train_scopes: variable scopes to train.
    """
    self.vars_to_restore = slim.get_variables_to_restore(
        exclude=restore_scope_exclude)
    self.vars_to_train = []
    for scope in train_scopes:
      variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope)
      self.vars_to_train.extend(variables)
    if not self.vars_to_train:
      self.vars_to_train = None

  def compute_losses(self, anchor_feats, pos_feats, neg_feats, endpoints):
    """Compute training losses.

    Override only when non-standard loss for a particular model.

    Args:
      anchor_feats: features for anchor batch.
      pos_feats: features for positive batch.
      neg_feats: features for negative batch.
      pred_logits: prediction logits.
      endpoints: endpoints from the model.
    Returns:
      computed losses.
    """
    triplet_loss = losses.triplet_loss(anchor_feats, pos_feats, neg_feats)
    slim.losses.add_loss(triplet_loss)
    tf.scalar_summary("losses/triplet_loss", triplet_loss)

  def train(self, train_anchor_batch, train_pos_batch, train_neg_batch,
            model_params, train_params):
    """Training process of the matcher.

    Each input data should have same shape.

    Args:
      train_anchor_batch: anchor batch.
      train_pos_batch: positive batch.
      train_neg_batch: negative batch.
      model_params: commons.ModelParams object.
      train_params: commons.TrainTestParams object.
    """
    # get embedding for all batches.
    all_batches = tf.concat(
        0, [train_anchor_batch, train_pos_batch, train_neg_batch])
    all_feats, endpoints = self.build_model(all_batches, model_params)
    anchor_feats, pos_feats, neg_feats = tf.split(0, 3, all_feats)
    self.set_key_vars(train_params.restore_scopes_exclude,
                      train_params.train_scopes)
    self.compute_losses(anchor_feats, pos_feats, neg_feats, endpoints)
    init_fn = None
    if train_params.fine_tune:
      init_fn = slim.assign_from_checkpoint_fn(train_params.custom["model_fn"],
                                               self.vars_to_restore)
    elif not train_params.resume_training:
      data_manager.remove_dir(train_params.train_log_dir)
    total_loss = slim.losses.get_total_loss(
        add_regularization_losses=train_params.use_regularization)
    base_model.train_model_given_loss(
        total_loss, self.vars_to_train, train_params, init_fn=init_fn)

  def test(self, gal_data, gal_labels, probe_data, probe_labels, model_params,
           test_params):
    """Testing process of the classifier.

    Args:
      gal_data: gallery data as numpy array.
      gal_labels: gallery labels.
      probe_data: probe data as numpy array.
      probe_labels: probe labels.
      model_params: commons.ModelParams object.
      test_params: commons.TrainTestParams object.
    """
    data_shape = gal_data.shape
    data_shape[0] = None
    inputs = tf.placeholder(tf.float32, shape=data_shape)
    self.input_tensor_name = inputs.name
    feats, _ = self.build_model(inputs, model_params)
    gal_feats = self.get_output(gal_data, feats.name)
    probe_feats = self.get_output(probe_data, feats.name)
    save_prefix = os.path.join(test_params.test_log_dir,
                               test_params.custom["eval_name"])
    dist_mat = search_tools.comp_distmat(
        probe_feats, gal_feats, dist_type=search_tools.DistType.L2)
    search_tools.evaluate(
        test_params.custom["eval_name"],
        dist_mat,
        np.asarray(gal_labels),
        np.asarray(probe_labels),
        save_fn_prefix=save_prefix)

  def load_model_from_checkpoint_fn(self, model_fn):
    """Load weights from file and keep in memory.

    Args:
      model_fn: saved model file.
    """
    if self.vars_to_restore is None:
      self.vars_to_restore = slim.get_variables()
    restore_fn = slim.assign_from_checkpoint_fn(model_fn, self.vars_to_restore)
    self.sess = tf.Session()
    print "class session created."
    print "restoring model from {}".format(model_fn)
    restore_fn(self.sess)
    print "model restored."

  def load_model_from_pb(self, pb_fn):
    """Load model data from a binary protobuf file.

    Args:
      pb_fn: protobuf file.
    """
    pass

  def get_output(self, input_data, target_tensor_name):
    """Get output from a specified tensor.

    Args:
      input_data: data to input.
      target_tensor_name: target tensor to evaluate.
    Returns:
      evaluated tensor value.
    """
    return base_model.eval_tensor(self.sess, self.input_tensor_name,
                                  input_data, target_tensor_name)


def main(_):
  # create model object.
  my_matcher = DMMatcher()
  # load data.
  # set model params.
  model_params = commons.ModelParams(
      "demo_model", model_type=commons.NetNames.CUSTOM, cls_num=10)
  # train.
  train_test_params = commons.TrainTestParams("", 1000)
  my_matcher.train(None, None, None, model_params, train_test_params)
  # test.
  my_matcher.test(None, None, None, None, model_params, train_test_params)


if __name__ == "__main__":
  tf.app.run()
