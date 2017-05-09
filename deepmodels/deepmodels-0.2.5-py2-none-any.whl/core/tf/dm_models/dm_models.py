"""Manager for deepmodels models.
"""

from ... import commons

import dm_vgg
import dm_inception


def get_dm_model(model_type):
  """A factory to spawn deepmodels.

  Args:
    model_type: type of network model.
  Returns:
    corresponding deepmodel model object.
  """
  if commons.is_inception_model(model_type):
    incep = dm_inception.InceptionDM(model_type)
    return incep
  elif commons.is_vgg_model(model_type):
    vgg = dm_vgg.VGGDM(model_type)
    return vgg
  else:
    raise ValueError("not supported model type.")
