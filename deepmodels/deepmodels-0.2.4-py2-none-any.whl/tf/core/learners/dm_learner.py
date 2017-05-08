"""Base class for learners in deepmodels.
"""

import abc
import os

import tensorflow as tf
import tensorflow.contrib.slim as slim

from deepmodels.tf.core import commons
from deepmodels.tf.core import base_model
from deepmodels.tf.core.dm_models import common as model_common


class DMLearner(object):
  """Base class for deepmodels learners.

  Attributes:
    input_tensor_name: name of input tensor, can be set to a custom name.
    output_tensor_name: name of output tensor.
    vars_to_train: variables to train.
    vars_to_restore: variables to restore from a model file.
    sess: tf.Session object to perserve a session for constant prediction.
  """
  __metaclass__ = abc.ABCMeta

  input_tensor_name = ""
  output_tensor_names = []
  vars_to_train = None
  vars_to_restore = None
  sess = None
  dm_model = None
  # final output tensor name.
  model_pred_tensor_name = ""

  def __init__(self, dm_model_):
    """Initialization.

    Args:
      dm_model_: deep model object.
    """
    self.set_dm_model(dm_model_)
    self.sess = tf.Session()
    print "class session created."

  def __del__(self):
    if self.sess is not None:
      self.sess.close()

  def check_dm_model_exist(self):
    """Check if dm_model exists.

    Enforce practice of using dm_model.
    """
    assert self.dm_model is not None, "dm_model can not be None"

  def set_dm_model(self, dm_model):
    """Use a dm model class.
    """
    assert isinstance(
        dm_model,
        model_common.NetworkDM), "dm_model needs to be a subclass of NetworkDM"
    self.dm_model = dm_model

  def set_key_vars(self, restore_scope_exclude, train_scopes):
    """Set critical variables for relevant tasks.

    Set vars_to_train and vars_to_restore.
    Called after build_model.

    Args:
      restore_scope_exclude: variable scopes to exclude for restoring.
      train_scopes: variable scopes to train.
    """
    self.dm_model.use_graph()
    self.vars_to_restore = slim.get_variables_to_restore(
        exclude=restore_scope_exclude)
    self.vars_to_train = []
    if train_scopes is not None:
      for scope in train_scopes:
        variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope)
        self.vars_to_train.extend(variables)
    if not self.vars_to_train:
      print "[set_key_vars: info] No variables to train were defined." \
            " Will train ALL variables."
      self.vars_to_train = None
    #base_model.print_variable_names(self.vars_to_train)

  def build_model(self, inputs):
    """Construct network graph using dm_model build_model().

    The internal input/output_tensor_name will be set based on
    dm_model.net_params.input/output_layer_name from endpoints.

    Args:
      inputs: input data, either data vectors or images.
    Returns:
      prediction and endpoints.
    """
    self.check_dm_model_exist()
    self.dm_model.use_graph()
    outputs, endpoints = self.dm_model.build_model(inputs)
    self.model_pred_tensor_name = outputs.name
    if self.dm_model.net_params.input_layer_name != "":
      self.input_tensor_name = endpoints[
          self.dm_model.net_params.input_layer_name].name
    else:
      self.input_tensor_name = inputs.name
    if self.dm_model.net_params.output_layer_names:
      for layer_name in self.dm_model.net_params.output_layer_names:
        self.output_tensor_names.append(endpoints[layer_name].name)
    else:
      self.output_tensor_names = [outputs.name]
    return outputs, endpoints

  def start(self):
    """Prepare learner.
    """
    self.check_dm_model_exist()
    self.dm_model.use_graph()
    # if in test mode, load weights.
    if self.dm_model.net_params.model_mode == commons.ModelMode.TEST:
      input_imgs = tf.placeholder(
          dtype=tf.float32,
          shape=(None, self.dm_model.net_params.input_img_height,
                 self.dm_model.net_params.input_img_width, 3),
          name="test_input")
      self.build_model(input_imgs)
      self.set_key_vars(self.dm_model.restore_scope_exclude, None)
      self.load_model_from_checkpoint_fn(self.dm_model.net_weight_fn)
      print "learner loaded from file: {}".format(self.dm_model.net_weight_fn)

  def get_outputs(self, input_data, preprocessed=True, target_tensor_names=[]):
    """Get outputs from a list of tensors.

    Args:
      input_data: raw network input as numpy array.
      preprocessed: if the data has been preprocessed.
      target_tensor_names: target tensors to evaluate.
      Use internal output_tensor_name as default.
    Returns:
      evaluated tensor values.
    """
    self.check_dm_model_exist()
    self.dm_model.use_graph()
    if not preprocessed:
      input_data = self.dm_model.preprocess(input_data)
    assert input_data.ndim == 4, "input data to get_output must have rank 4"
    if not target_tensor_names:
      target_tensor_names = self.output_tensor_names
    tensor_vals = []
    for tensor_name in target_tensor_names:
      cur_tensor_name = tensor_name
      tensor_val = base_model.eval_tensor(self.sess, self.input_tensor_name,
                                          input_data, cur_tensor_name)
      tensor_vals.append(tensor_val)
    return tensor_vals

  def load_model_from_checkpoint_fn(self, model_fn):
    """Load weights from file and keep in memory.

    Args:
      model_fn: saved model file.
    """
    self.dm_model.use_graph()
    print "start loading from checkpoint file..."
    if self.vars_to_restore is None:
      self.vars_to_restore = slim.get_variables()
    restore_fn = slim.assign_from_checkpoint_fn(model_fn, self.vars_to_restore)
    print "restoring model from {}".format(model_fn)
    restore_fn(self.sess)
    print "model restored."

  def load_model_from_pb(self, pb_fn):
    """Load model data from a binary protobuf file.

    Args:
      pb_fn: protobuf file.
    """
    pass
