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

from TransportMaps.Functionals.FunctionBase import *

__all__ = ['LogLikelihood']

class LogLikelihood(Function):
    r""" Abstract class for log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})`

    Note that :math:`\log\pi:\mathbb{R}^d \rightarrow \mathbb{R}`
    is considered a function of :math:`{\bf x}`, while the
    data :math:`{\bf y}` is fixed.
    
    Args:
      y (:class:`ndarray<numpy.ndarray>`): data
      dim (int): input dimension $d$
    """
    def __init__(self, y, dim):
        super(LogLikelihood, self).__init__(dim)
        self.y = y

    def evaluate(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- function evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

    def grad_x(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- gradient evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

    def hess_x(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- Hessian evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")