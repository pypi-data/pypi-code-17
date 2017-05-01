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

import copy as cp

from TransportMaps.ObjectBase import TMO
from TransportMaps.Distributions import StandardNormalDistribution, \
    PushForwardTransportMapDistribution, PullBackTransportMapDistribution
from TransportMaps.Distributions.Decomposable import \
    SequentialHiddenMarkovChainDistribution
from TransportMaps.Maps import TransportMap, TriangularTransportMap, \
    CompositeTransportMap, ListCompositeTransportMap, PermutationTransportMap, \
    TriangularListStackedTransportMap
from TransportMaps.Maps.Decomposable import LiftedTransportMap

__all__ = ['SequentialHiddenMarkovChainIntegrator']

class SequentialHiddenMarkovChainIntegrator(TMO):
    r""" Perform the on-line assimilation of a sequential Hidded Markov Chain.

    Given the prior distribution on the hyper-parameters :math:`\pi(\Theta)`,
    provides the functions neccessary to assimilate new pieces of data or
    missing data 
    (defined in terms of transition densities
    :math:`\pi\left({\bf Z}_{k+1} \middle\vert {\bf Z}_k, \Theta \right)`
    and log-likelihoods
    :math:`\log \mathcal{L}\left({\bf y}_{k+1}\middle\vert {\bf Z}_{k+1}, \Theta\right)`),
    to return the map pushing forward :math:`\mathcal{N}(0,{\bf I})`
    to the smoothing distribution
    :math:`\pi\left(\Theta, {\bf Z}_\Lambda \middle\vert {\bf y}_\Xi \right)`
    and to return the maps pushing forward :math:`\mathcal{N}(0,{\bf I})`
    to the filtering/forecast distributions
    :math:`\{\pi\left(\Theta, {\bf Z}_k \middle\vert {\bf y}_{0:k} \right)\}_k`.

    For more details see also :cite:`Spantini2017` and the
    `tutorial <example-sequential-stocvol-6d.html>`_.

    Args:
      pi_hyper (:class:`Distribution<TransportMaps.Distributions.Distribution>`):
        prior distribution on the hyper-parameters :math:`\pi(\Theta)`
    """
    def __init__(self, pi_hyper=None):
        super(SequentialHiddenMarkovChainIntegrator,self).__init__()
        self.pi = SequentialHiddenMarkovChainDistribution([], [], pi_hyper)
        self.nsteps = -1
        
    def assimilate(self, pi, ll, tm, solve_params,
                   hyper_tm=None, regression_params=None, skip_initial=False):
        r""" Assimilate one piece of data :math:`\left( \pi\left({\bf Z}_{k+1} \middle\vert {\bf Z}_k, \Theta \right), \log \mathcal{L}\left({\bf y}_{k+1}\middle\vert {\bf Z}_{k+1}, \Theta\right) \right)`.

        Given the new piece of data
        :math:`\left( \pi\left({\bf Z}_{k+1} \middle\vert {\bf Z}_k, \Theta \right), \log \mathcal{L}\left({\bf y}_{k+1}\middle\vert {\bf Z}_{k+1}, \Theta\right) \right)`,
        retrieve the :math:`k`-th Markov component :math:`\pi^k` of :math:`\pi`,
        determine the transport map

        .. math::

           \mathfrak{M}_k({\boldsymbol \theta}, {\bf z}_k, {\bf z}_{k+1}) = \left[
           \begin{array}{l}
           \mathfrak{M}^\Theta_k({\boldsymbol \theta}) \\
           \mathfrak{M}^0_k({\boldsymbol \theta}, {\bf z}_k, {\bf z}_{k+1}) \\
           \mathfrak{M}^1_k({\boldsymbol \theta}, {\bf z}_{k+1})
           \end{array}
           \right] = Q \circ R_k \circ Q

        that pushes forward :math:`\mathcal{N}(0,{\bf I})` to :math:`\pi^k`, and
        embed it into the linear map which will remove the desired conditional
        dependencies from :math:`\pi`.
        
        Optionally, it will also compress the maps
        :math:`\mathfrak{M}_{0}^\Theta \circ \ldots \circ \mathfrak{M}_{k-1}^\Theta`
        into the map :math:`\mathfrak{H}_{k-1}` in order to speed up the
        evaluation of the :math:`k`-th Markov component :math:`\pi^k`.

        Args:
          pi (:class:`Distribution<TransportMaps.Distributions.Distribution>`):
            transition distribution
            :math:`\pi\left({\bf Z}_{k+1} \middle\vert {\bf Z}_k, \Theta \right)`
          ll (:class:`LogLikelihood<TransportMaps.Functionals.LogLikelihood>`):
            log-likelihood
            :math:`\log \mathcal{L}\left({\bf y}_{k+1}\middle\vert {\bf Z}_{k+1}, \Theta\right)`. The value ``None`` stands for missing observation.
          tm (:class:`TransportMap<TransportMaps.Maps.TransportMap>`):
            transport map :math:`R_k`
          solve_params (dict): parameters to be passed to
            :func:`minimize_kl_divergence<TransportMaps.Maps.TransportMap.minimize_kl_divergence>`
          hyper_tm (:class:`TransportMap<TransportMaps.Maps.TransportMap>`):
            transport map :math:`\mathfrak{H}_{k-1}`
          regression_params (dict): parameters to be passed to
            :func:`regression<TransportMaps.Maps.TransportMap.regression>` during
            the determination of :math:`\mathfrak{H}_{k-1}`
          skip_initial (bool): whether to skip the approximation of
            :math:`\pi\left(\Theta, {\bf Z}_0 \middle\vert {\bf y}_0 \right)` in the first step.
        """
        # Append transition and log-likelihood in self.pi
        self.pi.append(pi, ll)
        self.nsteps += 1
        # Approximation
        if not skip_initial and self.nsteps == 0:
            # If step zero, then just approximate self.pi
            rho = StandardNormalDistribution(self.pi.dim)
            push_tm_rho = PushForwardTransportMapDistribution(tm, rho)
            log = push_tm_rho.minimize_kl_divergence(
                self.pi, **solve_params)
            self.T0 = tm
        elif self.nsteps == 1:
            # If step one, then approximate 0-th Markov component
            hdim = self.pi.hyper_dim
            sdim = self.pi.state_dim
            pi0 = self.pi.get_MarkovComponent(0)
            self.rho_mk = StandardNormalDistribution(pi0.dim)
            self.Q = PermutationTransportMap(
                list(range(hdim)) + \
                list(range(hdim+sdim, hdim+2*sdim)) + \
                list(range(hdim, hdim+sdim)) )
            pull_Q_pi0 = PullBackTransportMapDistribution(self.Q, pi0)
            push_tm_rho = PushForwardTransportMapDistribution(tm, self.rho_mk)
            log = push_tm_rho.minimize_kl_divergence(
                pull_Q_pi0, **solve_params)
            # H_list contains the hyper-parameters maps H
            # R_list contains the lower triangular maps R
            # M_list contains the generalized lower triangular maps M
            # L_list contains the lifted maps
            self.H_list = [ TriangularTransportMap( tm.active_vars[:hdim],
                                                    tm.approx_list[:hdim] ) ]
            self.R_list = [ tm ]
            self.M_list = [ ListCompositeTransportMap([self.Q, tm, self.Q]) ]
            self.L_list = [ LiftedTransportMap(0, self.M_list[0], self.pi.dim, hdim) ]
        elif self.nsteps > 1:
            # If step k, then approximate the (k-1)-th Markov component
            hdim = self.pi.hyper_dim
            sdim = self.pi.state_dim
            if self.nsteps > 2 and hyper_tm is not None:
                hyper_tm.regression(
                    self.H_list[-1], **regression_params)
                self.H_list[-1] = hyper_tm
            Mkm1 = TransportMap( self.R_list[-1].active_vars[hdim:hdim+sdim],
                                 self.R_list[-1].approx_list[hdim:hdim+sdim] )
            pik = self.pi.get_MarkovComponent(
                self.nsteps-1, state_map=Mkm1, hyper_map=self.H_list[-1] )
            pull_Q_pik = PullBackTransportMapDistribution(self.Q, pik)
            push_tm_rho = PushForwardTransportMapDistribution(tm, self.rho_mk)
            log = push_tm_rho.minimize_kl_divergence(
                pull_Q_pik, **solve_params)
            self.R_list.append( tm )
            self.M_list.append( ListCompositeTransportMap([self.Q, tm, self.Q]) )
            # Update dimension of all lifted maps
            for L in self.L_list:
                L.dim = L.dim_in = L.dim_out = self.pi.dim
            self.L_list.append( LiftedTransportMap(
                self.nsteps-1, self.M_list[-1], self.pi.dim, hdim) )
            # Store next hyper map composition
            self.H_list.append( CompositeTransportMap(
                self.H_list[-1], TriangularTransportMap(
                    self.R_list[-1].active_vars[:hdim],
                    self.R_list[-1].approx_list[:hdim] ) ) )

    def get_smoothing_map(self):
        r""" Returns the map :math:`\mathfrak{T}` pushing forward :math:`\mathcal{N}(0,{\bf I})` to the smoothing distribution :math:`\pi\left(\Theta, {\bf Z}_\Lambda \middle\vert {\bf y}_\Xi\right)`.

        The map :math:`\mathfrak{T}` is given by the composition
        :math:`T_0 \circ \cdots \circ T_{k-1}` maps constructed in
        :math:`k` assimilation steps.

        Returns:
          (:class:`TransportMap<TransportMaps.Maps.TransportMap>`) -- the map :math:`\mathfrak{T}`
        """
        if self.nsteps > 0:
            return ListCompositeTransportMap( self.L_list )
        elif self.nsteps == 0:
            return self.T0
        else:
            raise RuntimeError("No step assimilated yet!")

    def get_filtering_map(self, k):
        r""" Returns the map :math:`\widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1})` pushing forward :math:`\mathcal{N}(0,{\bf I})` to the filtering/forecast distribution :math:`\pi\left(\Theta, {\bf Z}_k \middle\vert {\bf y}_{0:k}\right)`.

        The maps :math:`\widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1})`
        are defined as follows:

        .. math::

           \widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1}) = 
           \left[\begin{array}{l}
           \mathfrak{M}_0^\Theta \circ \cdots \circ \mathfrak{M}_{k}^\Theta ({\bf x}_\theta) \\
           \mathfrak{M}_k^1\left({\bf x}_\theta, {\bf x}_{k+1}\right)
           \end{array}\right] =
           \left[\begin{array}{l}
           \mathfrak{H}_{k}({\bf x}_\theta) \\
           \mathfrak{M}_k^1\left({\bf x}_\theta, {\bf x}_{k+1}\right)
           \end{array}\right]

        Returns:
          (:class:`TransportMap<TransportMaps.Maps.TransportMap>`) -- transport map :math:`\widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1})`
        """
        if k == 0:
            return self.T0
        else:
            hdim = self.pi.hyper_dim
            sdim = self.pi.state_dim
            H = self.H_list[k-1]
            R = self.R_list[k-1]
            Rkp1 = TriangularTransportMap( R.active_vars[hdim:hdim+sdim],
                                           R.approx_list[hdim:hdim+sdim] )
            F = TriangularListStackedTransportMap( [H, Rkp1] )
            return F

    def get_filtering_map_list(self):
        r""" Returns the maps :math:`\{ \widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1}) \}_{i=0}^{k-1}` pushing forward :math:`\mathcal{N}(0,{\bf I})` to the filtering/forecast distributions :math:`\{\pi\left(\Theta, {\bf Z}_k \middle\vert {\bf y}_{0:k} \right)\}_k`.

        The maps :math:`\widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1})`
        are defined as follows:

        .. math::

           \widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1}) = 
           \left[\begin{array}{l}
           \mathfrak{M}_0^\Theta \circ \cdots \circ \mathfrak{M}_{k}^\Theta ({\bf x}_\theta) \\
           \mathfrak{M}_k^1\left({\bf x}_\theta, {\bf x}_{k+1}\right)
           \end{array}\right] =
           \left[\begin{array}{l}
           \mathfrak{H}_{k}({\bf x}_\theta) \\
           \mathfrak{M}_k^1\left({\bf x}_\theta, {\bf x}_{k+1}\right)
           \end{array}\right]

        Returns:
          (:class:`list` of :class:`TransportMap<TransportMaps.Maps.TransportMap>`) -- list of transport maps :math:`\widetilde{\mathfrak{M}}_k({\bf x}_\theta, {\bf x}_{k+1})`
        """
        return [ self.get_filtering_map(k) for k in range(self.nsteps+1) ]