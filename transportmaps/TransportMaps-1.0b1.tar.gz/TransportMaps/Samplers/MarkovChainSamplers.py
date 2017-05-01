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
# Author: Transport Map Team
# Website: transport-maps.mit.edu
# Support: transport-maps.mit.edu/qa/
#

import numpy as np
import scipy.stats as stats

from TransportMaps import mpi_eval
from TransportMaps.Samplers.SamplerBase import *

__all__ = ['MetropolisHastingsIndependentProposalsSampler']

class MetropolisHastingsIndependentProposalsSampler(Sampler):
    r""" Metropolis-Hastings with independent proposal sampler of distribution ``d``, with proposal distribution ``d_prop``

    Args:
      d (Distributions.Distribution): distribution to sample from
      d_prop (Distributions.Distribution): proposal distribution
    """
    def __init__(self, d, d_prop):
        if d.dim != d_prop.dim:
            raise ValueError("Dimension of the densities ``d`` and ``d_prop`` must " + \
                             "be the same")
        super(MetropolisHastingsIndependentProposalsSampler, self).__init__(d)
        self.prop_distribution = d_prop

    def rvs(self, m, burnin=0, x0=None, mpi_pool_tuple=(None,None)):
        r""" Generate a Markov Chain of :math:`m` equally weighted samples from the distribution ``d``

        Args:
          m (int): number of samples to generate
          burnin (int): number of burnin samples
          x0 (:class:`ndarray<numpy.ndarray>` [:math:`1,d`]): initial chain value
          mpi_pool_tuple (:class:`tuple` [2] of :class:`mpi_map.MPI_Pool<mpi_map.MPI_Pool>`):
            pool of processes to be used for the evaluation of ``d`` and ``prop_d``

        Returns:
          (:class:`tuple` (:class:`ndarray<numpy.ndarray>` [:math:`m,d`],
            :class:`ndarray<numpy.ndarray>` [:math:`m`])) -- list of
            points and weights
        """
        # Logging vars
        log_time_span = max((m+burnin)//100, 1)
        last_log = 0
        nrej = 0
        # Init
        samps = self.prop_distribution.rvs(m+burnin+1,
                                           mpi_pool=mpi_pool_tuple[1])
        if x0 is not None:
            samps[0,:] = x0
        scatter_tuple = (['x'], [samps])
        d_log_pdf_Y = mpi_eval("log_pdf", scatter_tuple=scatter_tuple,
                               obj=self.distribution, mpi_pool=mpi_pool_tuple[0])
        prop_d_log_pdf_Y = mpi_eval("log_pdf", scatter_tuple=scatter_tuple,
                                    obj=self.prop_distribution,
                                    mpi_pool=mpi_pool_tuple[1])
        xt_idx = 0
        for i in range(1,m+burnin+1):
            log_rho = min( d_log_pdf_Y[i] + prop_d_log_pdf_Y[xt_idx] - \
                           (d_log_pdf_Y[xt_idx] + prop_d_log_pdf_Y[i]) , 0 )
            if stats.bernoulli(np.exp(log_rho)).rvs(1): # Accept
                xt_idx = i
            else:
                nrej += 1
                samps[i,:] = samps[xt_idx,:]
            # Logging
            if i == last_log + log_time_span:
                rate = float(i-nrej)/float(i)*100.
                self.logger.debug("Sample %i/%i - " % (i,m+burnin) + \
                                  "Acceptance rate %2.1f%%" % rate )
                last_log = i
        return (samps[1+burnin:,:], np.ones(m)/float(m))