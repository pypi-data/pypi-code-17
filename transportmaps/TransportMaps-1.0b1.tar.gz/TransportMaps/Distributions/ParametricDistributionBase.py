#
# This file is part of TransportMaps.
#
# TransportMaps is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TransportMaps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with TransportMaps.  If not, see <http://www.gnu.org/licenses/>.
#
# Transport Maps Library
# Copyright (C) 2015-2017 Massachusetts Institute of Technology
# Uncertainty Quantification group
# Department of Aeronautics and Astronautics
#
# Authors: Transport Map Team
# Website: transport-maps.mit.edu
# Support: transport-maps.mit.edu/qa/
#

import warnings

from TransportMaps.Distributions.DistributionBase import *

__all__ = ['ParametricDistribution']

class ParametricDistribution(Distribution):
    r""" Parametric distribution :math:`\pi_{\bf a}`.
    """

    def get_coeffs(self):
        r""" [Abstract] Get the coefficients :math:`{\bf a}` of the distribution

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`N`]) -- coefficients

        Raises:
          NotImplementedError: the method needs to be defined in the sub-classes
        """
        raise NotImplementedError("The method is not implemented for this distribution")

    def get_n_coeffs(self):
        r""" [Abstract] Get the number :math:`N` of coefficients

        Returns:
          (int) -- number of coefficients.

        Raises:
          NotImplementedError: the method needs to be defined in the sub-classes
        """
        raise NotImplementedError("The method is not implemented for this distribution")

    def set_coeffs(self):
        r""" [Abstract] Set the coefficients :math:`{\bf a}` of the distribution

        Args:
          a (:class:`ndarray<numpy.ndarray>` [:math:`N`]) -- coefficients

        Raises:
          NotImplementedError: the method needs to be defined in the sub-classes
        """
        raise NotImplementedError("The method is not implemented for this distribution")

    def grad_a_log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" [Abstract] Evaluate :math:`\nabla_{\bf a} \log \pi({\bf x})`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,N`]) -- :math:`\nabla_{\bf a} \log \pi({\bf x})`

        Raises:
          NotImplementedError: the method needs to be defined in the sub-classes
        """
        raise NotImplementedError("The method is not implemented for this distribution")

    def hess_a_log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" [Abstract] Evaluate :math:`\nabla^2_{\bf a} \log \pi({\bf x})`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,N`]) -- :math:`\nabla^2_{\bf a} \log \pi({\bf x})`

        Raises:
          NotImplementedError: the method needs to be defined in the sub-classes
        """
        raise NotImplementedError("The method is not implemented for this distribution")

    def minimize_kl_divergence(self, tar):
        r""" [Abstract] Solve :math:`\arg \min_{\bf a}\mathcal{D}_{KL}(\pi_{\bf a}, \pi_{\rm tar})`

        Args:
          tar (:class:`Distribution<TransportMaps.Distributions.Distribution>`): target distribution

        Raises:
          NotImplementedError: the method needs to be defined in the sub-classes
        """
        raise NotImplementedError("The method is not implemented for this distribution")
