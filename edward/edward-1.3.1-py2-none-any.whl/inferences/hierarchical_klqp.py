from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six
import tensorflow as tf

from edward.inferences.gan_inference import GANInference
from edward.models import RandomVariable
from edward.util import check_latent_vars, copy, get_session


# TODO redesign
class HierarchicalKLqp(GANInference):
  """Variational inference with hierarchical variational models
  (Ranganath et al., 2016).

  It minimizes the KL divergence

  .. math::

    \\text{KL}( q(z, \lambda; \theta) \| p(z \mid x) r(\lambda\mid z; \phi) ),

  TODO
  where :math:`z` are local variables associated to a data point and
  :math:`\\beta` are global variables shared across data points.

  TODO
  Global latent variables require ``log_prob()`` and need to return a
  random sample when fetched from the graph. Local latent variables
  and observed variables require only a random sample when fetched
  from the graph. (This is true for both :math:`p` and :math:`q`.)

  TODO
  All variational factors must be reparameterizable: each of the
  random variables (``rv``) satisfies ``rv.is_reparameterized`` and
  ``rv.is_continuous``.
  """
  def __init__(self, latent_vars=None, data=None, auxiliary_vars=None):
    """
    Parameters
    ----------
    auxiliary_vars : dict of RandomVariable to RandomVariable, optional
      TODO
      Identifying which variables in ``latent_vars`` are global
      variables, shared across data points. These will not be
      encompassed in the ratio estimation problem, and will be
      estimated with tractable variational approximations.
    """
    if auxiliary_vars is None:
      auxiliary_vars = {}

    check_latent_vars(auxiliary_vars)
    self.auxiliary_vars = auxiliary_vars
    latent_vars_temp = latent_vars
    self.latent_vars = latent_vars.copy()
    self.latent_vars.update(auxiliary_vars)
    super(HierarchicalKLqp, self).__init__(*args, **kwargs)
