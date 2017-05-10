"""Inception models.
"""

import os
import sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(cur_dir, "../")
sys.path.insert(0, parent_dir)
sys.path.insert(1, os.path.join(parent_dir, "models/slim/"))

from nets import nets_factory
from preprocessing import preprocessing_factory

from ... import commons
from .. import model_zoo
from ....tools import data_manager


class InceptionDM(model_zoo.NetworkDM):
  """Inception model, including v1, v2 and v3.
  """
  inception_v1_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[
          commons.ModelTypes.INCEPTION_V1],
      model_type=commons.ModelTypes.INCEPTION_V1,
      input_img_width=224,
      input_img_height=224,
      cls_num=1001)

  inception_v2_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[
          commons.ModelTypes.INCEPTION_V2],
      model_type=commons.ModelTypes.INCEPTION_V2,
      input_img_width=224,
      input_img_height=224,
      cls_num=1001)

  inception_v3_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[
          commons.ModelTypes.INCEPTION_V3],
      model_type=commons.ModelTypes.INCEPTION_V3,
      input_img_width=299,
      input_img_height=299,
      cls_num=1001)

  inception_v4_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[
          commons.ModelTypes.INCEPTION_V4],
      model_type=commons.ModelTypes.INCEPTION_V4,
      input_img_width=299,
      input_img_height=299,
      cls_num=1001)

  def __init__(self, model_type=commons.ModelTypes.INCEPTION_V3):
    if model_type == commons.ModelTypes.INCEPTION_V1:
      self.net_params = self.inception_v1_params
    elif model_type == commons.ModelTypes.INCEPTION_V2:
      self.net_params = self.inception_v2_params
    elif model_type == commons.ModelTypes.INCEPTION_V3:
      self.net_params = self.inception_v3_params
    elif model_type == commons.ModelTypes.INCEPTION_V4:
      self.net_params = self.inception_v4_params
    else:
      raise ValueError("not a valid inception model type")
    self.net_graph_fn = ""
    self.net_weight_fn = model_zoo.get_builtin_net_weights_fn(
        self.net_params.model_type)
    self.net_label_names = self.get_label_names()

  def get_preprocess_fn(self):
    preprocess_fn = model_zoo.get_builtin_net_preprocess_fn(
        self.net_params.model_type, self.net_params.model_mode)
    return preprocess_fn

  def get_label_names(self):
    proj_dir = data_manager.get_project_dir()
    label_fn = os.path.join(proj_dir, "models/inception/inception_labels.txt")
    label_name_dict = {}
    with open(label_fn, "r") as f:
      label_str = f.read()
      label_name_dict = eval(label_str)
    return label_name_dict

  def build_model(self, inputs, template_type=commons.TemplateType.Classifier):
    if template_type == commons.TemplateType.Classifier:
      logits, endpoints = model_zoo.create_builtin_net(
          self.net_params.model_type, inputs, self.net_params.cls_num,
          self.net_params.model_mode)
      return logits, endpoints
    else:
      raise ValueError("unsupported template type.")
