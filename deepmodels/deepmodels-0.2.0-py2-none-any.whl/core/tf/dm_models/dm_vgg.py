"""DeepModels version of VGG16.
"""

import os
import sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(cur_dir, "../")
sys.path.insert(0, parent_dir)
sys.path.insert(1, os.path.join(parent_dir, "models/slim/"))

# import tensorflow as tf
# import tensorflow.contrib.slim as slim

from nets import nets_factory
from preprocessing import preprocessing_factory

from ... import commons
from .. import model_zoo
from ....tools import data_manager


class VGGDM(model_zoo.NetworkDM):
  """DeepModels version of vgg, including 16 and 19.
  """
  vgg16_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[commons.ModelTypes.VGG16],
      model_type=commons.ModelTypes.VGG16,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)
  vgg19_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[commons.ModelTypes.VGG19],
      model_type=commons.ModelTypes.VGG19,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)

  def __init__(self, net_type=commons.ModelTypes.VGG16):
    if net_type == commons.ModelTypes.VGG16:
      self.net_params = self.vgg16_params
    elif net_type == commons.ModelTypes.VGG19:
      self.net_params = self.vgg19_params
    else:
      raise ValueError("incorrect vgg type.")
    self.net_graph_fn = ""
    self.net_weight_fn = model_zoo.get_builtin_net_weights_fn(
        self.net_params.model_type)

  def build_model(self, inputs, template_type=commons.TemplateType.Classifier):
    if template_type == commons.TemplateType.Classifier:
      logits, endpoints = model_zoo.create_builtin_net(
          self.net_params.model_type, inputs, self.net_params.cls_num,
          self.net_params.model_mode)
      return logits, endpoints
    else:
      raise ValueError("unsupported template type.")

  def get_preprocess_fn(self):
    preprocess_fn = preprocessing_factory.get_preprocessing(
        self.net_params.model_name,
        is_training=self.net_params.model_mode != commons.ModelMode.TEST)
    return preprocess_fn

  def get_label_names(self):
    proj_dir = data_manager.get_project_dir()\
    #TODO(jiefeng): check if vgg19 uses the same labels.
    label_fn = os.path.join(proj_dir, "models/vgg/vgg_16_labels.txt")
    label_name_dict = {}
    with open(label_fn, "r") as f:
      label_str = f.read()
      label_name_dict = eval(label_str)
    return label_name_dict
