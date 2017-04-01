"""Inception Resnet models.
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


class InceptionResNetDM(model_zoo.NetworkDM):
  """Inception resnet model, only v2 now.
  """

  def __init__(self):
    net_type = commons.ModelTypes.INCEPTION_RESNET_V2
    self.net_params = commons.ModelParams(
        model_name=commons.ModelTypes.model_names[net_type],
        model_type=net_type,
        input_img_width=224,
        input_img_height=224,
        cls_num=1001)
    self.net_graph_fn = ""
    self.net_weight_fn = model_zoo.get_builtin_net_weights_fn(
        self.net_params.model_type)

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

  def build_model(self, inputs, template_type):
    logits, endpoints = model_zoo.create_builtin_net(
        self.net_params.model_type, inputs, self.net_params.cls_num,
        self.net_params.model_mode)
    return logits, endpoints
