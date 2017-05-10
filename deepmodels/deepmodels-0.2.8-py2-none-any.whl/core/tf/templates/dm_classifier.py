"""Template class for image classifier.
"""

import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from ... import commons
from .. import base_model
from .. import common_flags
from ....tools import data_manager

flags = tf.app.flags
FLAGS = flags.FLAGS


def comp_train_accuracy(pred_logits, label_batch):
  correct_prediction = tf.equal(tf.argmax(pred_logits, 1), label_batch)
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  tf.scalar_summary("eval/mean_clf_accuracy", accuracy)


# TODO(jiefeng): need a good way ensure user writes the exact same function
# header for overriding.
class DMClassifier(object):
  """Classifier template class.

  Work with general feature input or image feature.

  Attributes:
    input_tensor_name: name of input tensor, can be set to a custom name.
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
  dm_model = None

  def __init__(self):
    self.sess = tf.Session()

  def __del__(self):
    if self.sess is not None:
      self.sess.close()

  def set_dm_model(self, dm_model):
    """Use a dm model class.
    """
    self.dm_model = dm_model

  def build_model(self, inputs, model_params):
    """Construct deep model.

    Override to define a custom model.
    Put all graph construction here.

    Args:
      inputs: input data, either data vectors or images.
      model_params: model related parameters.
    Returns:
      prediction logits and endpoints.
    """
    if self.dm_model is not None:
      logits, endpoints = self.dm_model.build_model(inputs)
      return logits, endpoints

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

  def compute_losses(self, gt_labels, pred_logits, endpoints):
    """Compute training losses.

    Override only when non-standard loss for a particular model.

    Args:
      gt_labels: ground truth labels in one-hot encoding.
      pred_logits: prediction logits.
      endpoints: endpoints from the model.
    Returns:
      computed losses.
    """
    clf_loss = slim.losses.softmax_cross_entropy(
        pred_logits, gt_labels, weight=1.0, scope="clf_loss")
    tf.scalar_summary("losses/clf_loss", clf_loss)

  def train(self, train_input_batch, train_label_batch, model_params,
            train_params):
    """Training process of the classifier.

    Args:
      train_input_batch: input batch for training.
      train_label_batch: class id for training.
      model_params: commons.ModelParams object.
      train_params: commons.TrainTestParams object.
    """
    # add image summary.
    tf.image_summary("train images", train_input_batch)
    pred_logits, endpoints = self.build_model(train_input_batch, model_params)
    self.set_key_vars(train_params.restore_scopes_exclude,
                      train_params.train_scopes)
    comp_train_accuracy(pred_logits, train_label_batch)
    onehot_labels = slim.one_hot_encoding(train_label_batch,
                                          model_params.cls_num)
    self.compute_losses(onehot_labels, pred_logits, endpoints)
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

  def test(self, test_input_batch, test_label_batch, model_params,
           test_params):
    """Testing process of the classifier.

    Args:
      test_input_batch: input batch for testing.
      test_label_batch: class id for testing.
      model_params: commons.ModelParams object.
      test_params: commons.TrainTestParams object.
    """
    pred_logits, _ = self.build_model(test_input_batch, model_params)
    pred_cls = tf.argmax(pred_logits, 1)
    metric_args = {
        "eval/mean_clf_accuracy":
        slim.metrics.streaming_accuracy(pred_cls, test_label_batch)
    }
    base_model.test_model_given_metrics(metric_args, test_params)

  def load_model_from_checkpoint_fn(self, model_fn):
    """Load weights from file and keep in memory.

    Args:
      model_fn: saved model file.
    """
    if self.vars_to_restore is None:
      self.vars_to_restore = slim.get_variables()
    restore_fn = slim.assign_from_checkpoint_fn(model_fn, self.vars_to_restore)
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

  def predict(self, input_data):
    """Get prediction value from a tensor.

    Args:
      input_data: inputs as numpy array to predict.
    Returns:
      two matrices with each row for each sample and
    ranked label id and probability.
    """
    cur_graph = tf.get_default_graph()
    output_tensor = cur_graph.get_tensor_by_name(self.output_tensor_name)
    pred_prob_tensor = tf.nn.softmax(output_tensor)
    pred_probs = self.get_output(input_data, pred_prob_tensor.name)
    sorted_pred_labels = np.argsort(pred_probs, axis=1)[:, ::-1]
    sorted_pred_probs = np.sort(pred_probs, axis=1)[:, ::-1]
    return sorted_pred_labels, sorted_pred_probs


def main(_):
  # create model object.
  my_clf = DMClassifier()
  # load data.
  # set model params.
  model_params = commons.ModelParams(
      "demo_model", model_type=commons.NetNames.CUSTOM, cls_num=10)
  # train.
  train_test_params = commons.TrainTestParams("", 1000)
  my_clf.train(None, None, model_params, train_test_params)

  # test.
  my_clf.test(None, None, model_params, train_test_params)

  # predict.
  inputs = tf.Placeholder(tf.float32)
  my_clf.build_model(inputs, model_params)
  my_clf.get_output("")


if __name__ == "__main__":
  tf.app.run()
