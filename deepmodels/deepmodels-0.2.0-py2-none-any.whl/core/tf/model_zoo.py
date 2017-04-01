"""Definition of deep models.

Provide an organized structure for deep networks.
We will use existing slim model library so
will not reimplement them here.
"""

import os
import glob
import sys
cur_fn_path = os.path.realpath(__file__)
cur_fn_dir = os.path.dirname(cur_fn_path)
sys.path.insert(0, os.path.join(cur_fn_dir, "models/slim/"))

import tensorflow as tf
import tensorflow.contrib.slim as slim

from nets import nets_factory
from preprocessing import preprocessing_factory

from .. import commons
from ...tools import data_manager

# from dm_models import dm_vgg, dm_inception

# Params for various networks.
# net_params = {
#     commons.NetNames.CIFAR10: commons.ModelParams(
#         model_name="cifarnet",
#         model_type=commons.NetNames.CIFAR10,
#         input_img_width=32,
#         input_img_height=32,
#         cls_num=10),
#     commons.NetNames.INCEPTION_V1: commons.ModelParams(
#         model_name="inception_v1",
#         model_type=commons.NetNames.INCEPTION_V1,
#         input_img_width=224,
#         input_img_height=224,
#         cls_num=1001),
#     commons.NetNames.INCEPTION_V2: commons.ModelParams(
#         model_name="inception_v2",
#         model_type=commons.NetNames.INCEPTION_V2,
#         input_img_width=224,
#         input_img_height=224,
#         cls_num=1001),
#     commons.NetNames.INCEPTION_V3: commons.ModelParams(
#         model_name="inception_v3",
#         model_type=commons.NetNames.INCEPTION_V3,
#         input_img_width=299,
#         input_img_height=299,
#         cls_num=1001),
#     commons.NetNames.VGG_M: commons.ModelParams(
#         model_name="vgg_m",
#         model_type=commons.NetNames.VGG_M,
#         input_img_width=224,
#         input_img_height=224,
#         cls_num=1000),
#     commons.NetNames.VGG16: commons.ModelParams(
#         model_name="vgg_16",
#         model_type=commons.NetNames.VGG16,
#         input_img_width=224,
#         input_img_height=224,
#         cls_num=1000),
#     commons.NetNames.VGG19: commons.ModelParams(
#         model_name="vgg_19",
#         model_type=commons.NetNames.VGG19,
#         input_img_width=224,
#         input_img_height=224,
#         cls_num=1000),
#     commons.NetNames.ALEX_V2: commons.ModelParams(
#         model_name="alexnet_v2",
#         model_type=commons.NetNames.ALEX_V2,
#         input_img_width=224,
#         input_img_height=224,
#         cls_num=1000),
#     commons.NetNames.INCEPTION_RESNET_V2: commons.ModelParams(
#         model_name="inception_resnet_v2",
#         model_type=commons.NetNames.INCEPTION_RESNET_V2,
#         input_img_width=299,
#         input_img_height=299,
#         cls_num=1000)
# }


class NetworkDM(object):
  """Class template for metadata of a network.

  It contains information regarding the model itself,
  e.g. name, definition, labels etc.
  Good to be used together with a template to simplify process.
  """
  # network parameters.
  net_params = commons.ModelParams()
  # network data files.
  net_graph_fn = ""
  net_weight_fn = ""
  # mapping from predicted label to name string.
  net_label_names = {}

  def config_model(self, cls_num=None, mode=None):
    """Set model parameters.
    """
    if cls_num != None:
      self.net_params.cls_num = cls_num
    if mode != None:
      self.net_params.model_mode = mode

  def build_model(self, inputs, template_type=commons.TemplateType.Classifier):
    """Define network model.
    """
    pass

  def get_preprocess_fn(self):
    """Obtain a corresponding preprocess function.
    """
    pass

  def get_label_names(self):
    """Obtain corresponding label names.
    """
    pass


def is_tf_builtin_model_by_name(model_name):
  """Check if it is a built-in model from tf models.
  """
  tf_models = [
      "cifarnet", "inception_v1", "inception_v2", "inception_v3",
      "inception_v4", "vgg_16", "vgg_19", "alexnet_v2", "inception_resnet_v2"
  ]
  if model_name in tf_models:
    return True
  else:
    return False


def is_tf_builtin_model_by_type(model_type):
  """Check if it is a built-in model from tf models.
  """
  tf_models = [
      commons.ModelTypes.CIFAR10, commons.ModelTypes.INCEPTION_V1,
      commons.ModelTypes.INCEPTION_V2, commons.ModelTypes.INCEPTION_V3,
      commons.ModelTypes.INCEPTION_V4, commons.ModelTypes.VGG16,
      commons.ModelTypes.VGG19, commons.ModelTypes.ALEX_V2,
      commons.ModelTypes.INCEPTION_RESNET_V2
  ]
  if model_type in tf_models:
    return True
  else:
    return False


def create_builtin_net(model_type,
                       inputs,
                       cls_num,
                       mode=commons.ModelMode.TRAIN):
  """Build a network that is included in official model repo.

  Args:
    model_type: type of network.
    inputs: input tensor, batch or placeholder.
    cls_num: output class number.
    mode: model mode.
  Returns:
    net: network output.
    end_points: dictionary of named layer outputs.
  """
  if not is_tf_builtin_model_by_type(model_type):
    raise ValueError("net type is not supported.")

  # print "is training: {}".format(mode != commons.ModelMode.TEST)
  target_net = nets_factory.get_network_fn(
      commons.ModelTypes.model_names[model_type],
      cls_num,
      weight_decay=0.00004,
      is_training=mode != commons.ModelMode.TEST)
  logits, end_points = target_net(inputs)
  return logits, end_points


def get_builtin_net_weights_fn(model_type):
  """Retrieve built-in network weights file path.

  Used for loading weights.

  Args:
    model_type: type of network.
  Returns:
    network weight file.
  """
  if not is_tf_builtin_model_by_type(model_type):
    raise ValueError("net type is not supported.")
  proj_dir = data_manager.get_project_dir()
  ckpt_dir = os.path.join(proj_dir, "models/",
                          commons.ModelTypes.model_names[model_type])
  # if not os.path.exists(ckpt_dir):
  #   raise ValueError("Default model data directory {} not exist."
  #                    " Run script under DeepModels/Models/ to set up.".format(
  #                        ckpt_dir))

  # ckpts = glob.glob(os.path.join(ckpt_dir, "*.ckpt*"))
  # ckpt = ckpts[0]
  ckpt = os.path.join(ckpt_dir,
                      commons.ModelTypes.model_names[model_type] + ".ckpt")
  return ckpt


def get_builtin_net_preprocess_fn(model_type,
                                  model_mode=commons.ModelMode.TRAIN):
  """Perform preprocess for a network.

  Args:
    model_type: type of network.
    target_width: target image width.
    target_height: target image height.
    model_mode: mode of the model.
  Returns:
    preprocess function for the given network.
  """
  if not is_tf_builtin_model_by_type(model_type):
    raise ValueError("net type is not supported.")
  preprocess_fn = preprocessing_factory.get_preprocessing(
      commons.ModelTypes.model_names[model_type],
      is_training=model_mode != commons.ModelMode.TEST)
  return preprocess_fn


def apply_batch_net_preprocess(net_type,
                               inputs,
                               target_width,
                               target_height,
                               model_mode=commons.ModelMode.TRAIN):
  """Apply preprocess op to batch images.

  Args:
    net_type: type of network.
    inputs: batch images with shape (batch_size, h, w, ch).
    target_width: target image width.
    target_height: target image height.
    model_mode: mode of the model.
  Returns:
    preprocessed batch images.
  """
  pre_fn = get_builtin_net_preprocess_fn(net_type, model_mode)
  all_inputs = tf.unpack(inputs)
  processed_inputs = []
  for cur_input in all_inputs:
    new_input = pre_fn(cur_input, target_height, target_width)
    processed_inputs.append(new_input)
  new_inputs = tf.pack(processed_inputs)
  return new_inputs


# TODO(jiefeng): move to data related place?
# def net_label_names(net_type):
#   """Get label names for a network.

#   Args:
#     net_type: network type.
#   Returns:
#     a label to string dict for name mapping.
#   """
#   if net_type not in {
#       commons.ModelTypes.VGG16, commons.ModelTypes.INCEPTION_V3,
#       commons.ModelTypes.INCEPTION_V1
#   }:
#     raise ValueError("Only VGG16 labels are supported now.")
#   net_name = net_params[net_type].model_name
#   proj_dir = data_manager.get_project_dir()
#   label_fn = os.path.join(proj_dir, "models/{}/{}_labels.txt".format(net_name,
#                                                                      net_name))
#   label_name_dict = {}
#   with open(label_fn, "r") as f:
#     label_str = f.read()
#     label_name_dict = eval(label_str)
#     # label_names = f.readlines()
#     # label_name_dict = {i:label_names[i].rstrip() for i in range(len(label_names))}
#   return label_name_dict
