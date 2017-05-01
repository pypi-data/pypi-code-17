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

import numpy as np

from TransportMaps.Distributions.DistributionBase import *
from TransportMaps.Distributions.FrozenDistributions import StandardNormalDistribution

__all__ = ['MarkovChainDistribution',
           'SequentialHiddenMarkovChainDistribution',
           'MarkovComponentDistribution']

nax = np.newaxis

class MarkovChainDistribution(Distribution):
    r""" Distribution of a Markov process (optionally with hyper-parameters)

    For the index set :math:`A=[t_0,\ldots,t_k]` with :math:`t_0<t_1<\ldots <t_k`,
    and the user defined densities 
    :math:`f(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i})`,
    :math:`g(\Theta, {\bf Z}_{t_0})` and :math:`h(\Theta)`
    defines the distribution

    .. math::

       \pi(\Theta, {\bf Z}_A) = \left( \prod_{i=1}^k f(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i}) \right) g(\Theta, {\bf Z}_{t_0}) h(\Theta)

    associated to the process :math:`{\bf Z}_A`, where

    .. math::

       f(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i}) := \pi({\bf Z}_{t_i} \vert {\bf Z}_{t_{i-1}}, \Theta) \,, \\
       g(\Theta, {\bf Z}_{t_0}) := \pi({\bf Z}_{t_0} \vert \Theta) \\
       h(\Theta) := \pi(\Theta)

    .. note:: The argument inputs are assumed in the order as above
       (i.e. :math:`\Theta, {\bf Z}_A`).
       The conditional distribution
       :math:`g(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i})`
       is assumed to be extending the class :class:`Distribution` and have the
       same interface, where the input :math:`{\bf x}` contains both
       :math:`\Theta, {\bf Z}_{t_{i-1}}` and :math:`{\bf Z}_{t_i}`.

    Args:
      pi_list (:class:`list` of :class:`Distribution`): list of transition densities
        :math:`\{g(\Theta, {\bf Z}_{t_0}), f(\Theta, {\bf Z}_{t_{0}}, {\bf Z}_{t_1}), \ldots \}`
      pi_hyper (:class:`Distribution`): prior on hyper-parameters :math:`h(\Theta)`
    """
    def __init__(self, pi_list, pi_hyper=None):
        # Figure out dimension hyper-parameters
        if pi_hyper is None:
            hyper_dim = 0
        else:
            hyper_dim = pi_hyper.dim
        # Check consistency
        dim = hyper_dim
        for i, pi in enumerate(pi_list):
            if i == 0:
                self.state_dim = pi.dim - hyper_dim
                dim += self.state_dim
            else:
                if pi.dim != 2 * self.state_dim + hyper_dim:
                    raise ValueError("The dimension of the %d component is not consistent" % i)
                dim += self.state_dim
        # Init
        super(MarkovChainDistribution, self).__init__(dim)
        self.pi_list = pi_list
        self.pi_hyper = pi_hyper
        self.hyper_dim = hyper_dim

    def get_n_steps(self):
        r""" Returns the number of steps (time indices) :math:`\sharp A`.
        """
        return len(self.pi_list)

    def append(self, pi):
        r""" Append a new transition distribution :math:`g(\Theta, {\bf Z}_{t_{k}}, {\bf Z}_{t_{k+1}})`

        Args:
          pi (:class:`Distribution`): transition distribution
            :math:`g(\Theta, {\bf Z}_{t_{k}}, {\bf Z}_{t_{k+1}})`
        """
        if len(self.pi_list) == 0:
            self.state_dim = pi.dim - self.hyper_dim
        elif pi.dim != 2 * self.state_dim + self.hyper_dim:
            raise ValueError("The dimension of the new component is not consistent")
        self.pi_list.append( pi )
        self.dim += self.state_dim

    def log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" Evaluate :math:`\log \pi({\bf Z}_A, \Theta)`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- values of :math:`\log\pi`
            at the ``x`` points.
        """
        if x.shape[1] != self.dim:
            raise ValueError(
                "Input dimension %d != " % x.shape[1] + \
                "distribution dimension %d" % self.dim)
        out = np.zeros(x.shape[0])
        if self.pi_hyper is not None:
            out += self.pi_hyper.log_pdf(x[:,:self.hyper_dim], params, idxs_slice)
        if len(self.pi_list) > 0:
            out += self.pi_list[0].log_pdf(x[:,:(self.hyper_dim+self.state_dim)],
                                           params, idxs_slice)
        for i, pi in enumerate(self.pi_list[1:]):
            start_state = self.hyper_dim + i*self.state_dim
            stop_state = start_state + 2*self.state_dim
            xin = np.hstack( (x[:,:self.hyper_dim],
                              x[:,start_state:stop_state]) )
            out += pi.log_pdf( xin, params, idxs_slice )
        return out

    def grad_x_log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" Evaluate :math:`\nabla_{{\bf Z},\Theta}\log \pi({\bf Z}_A, \Theta)`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- values of
            :math:`\nabla_{{\bf Z},\Theta}\log\pi` at the ``x`` points.
        """
        if x.shape[1] != self.dim:
            raise ValueError(
                "Input dimension %d != " % x.shape[1] + \
                "distribution dimension %d" % self.dim)
        out = np.zeros((x.shape[0], self.dim))
        if self.pi_hyper is not None:
            out[:,:self.hyper_dim] = self.pi_hyper.grad_x_log_pdf(
                x[:,:self.hyper_dim], params, idxs_slice)
        if len(self.pi_list) > 0:
            out[:,:(self.hyper_dim+self.state_dim)] += \
                self.pi_list[0].grad_x_log_pdf(
                    x[:,:(self.hyper_dim+self.state_dim)], params, idxs_slice)
        for i, pi in enumerate(self.pi_list[1:]):
            start_state = self.hyper_dim + i*self.state_dim
            stop_state = start_state + 2*self.state_dim
            xin = np.hstack( (x[:,:self.hyper_dim],
                              x[:,start_state:stop_state]) )
            gx = pi.grad_x_log_pdf( xin, params, idxs_slice )
            out[:,:self.hyper_dim] += gx[:,:self.hyper_dim]
            out[:,start_state:stop_state] += gx[:,self.hyper_dim:]
        return out

    def hess_x_log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" Evaluate :math:`\nabla^2_{{\bf Z},\Theta}\log \pi({\bf Z}_A, \Theta)`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- values of
            :math:`\nabla^2_{{\bf Z},\Theta}\log\pi` at the ``x`` points.
        """
        if x.shape[1] != self.dim:
            raise ValueError(
                "Input dimension %d != " % x.shape[1] + \
                "distribution dimension %d" % self.dim)
        hdim = self.hyper_dim
        sdim = self.state_dim
        out = np.zeros((x.shape[0], self.dim, self.dim))
        if self.pi_hyper is not None:
            out[:,:hdim,:hdim] = self.pi_hyper.hess_x_log_pdf(
                x[:,:hdim], params, idxs_slice)
        if len(self.pi_list) > 0:
            out[:,:(hdim+sdim),:(hdim+sdim)] += \
                self.pi_list[0].hess_x_log_pdf(
                    x[:,:(hdim+sdim)], params, idxs_slice)
        for i, pi in enumerate(self.pi_list[1:]):
            s1 = hdim + i*sdim # Start state
            s2 = s1 + 2*sdim   # Stop state
            xin = np.hstack( (x[:,:hdim], x[:,s1:s2]) )
            hx = pi.hess_x_log_pdf( xin, params, idxs_slice )
            out[:,:hdim,:hdim] += hx[:,:hdim,:hdim]
            out[:,:hdim,s1:s2] += hx[:,:hdim,hdim:]
            out[:,s1:s2,:hdim] += hx[:,hdim:,:hdim]
            out[:,s1:s2,s1:s2] += hx[:,hdim:,hdim:]
        return out

class SequentialHiddenMarkovChainDistribution(MarkovChainDistribution):
    r""" Distribution of a sequential Hidden Markov chain model (optionally with hyper-parameters)

    For the index sets :math:`A=[t_0,\ldots,t_k]` with :math:`t_0<t_1<\ldots <t_k`, 
    :math:`B \subseteq A`, 
    the user defined transition densities (:class:`Distribution`)
    :math:`\{g(\Theta, {\bf Z}_{t_0}), f(\Theta, {\bf Z}_{t_{0}}, {\bf Z}_{1}), \ldots \}`,
    the prior :math:`\pi(\Theta)` and 
    the log-likelihoods (:class:`LogLikelihood<TransportMaps.Functionals.LogLikelihood>`)
    :math:`\{\log\mathcal{L}({\bf y}_t \vert \Theta, {\bf Z}_t)\}_{t\in B}`, defines the distribution

    .. math::

       \pi(\Theta, {\bf Z}_A \vert {\bf y}_B) =
         \left( \prod_{t\in B} \mathcal{L}({\bf y}_t \vert \Theta, {\bf Z}_t) \right)
         \left( \prod_{i=1}^k f(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i}) \right)
         g(\Theta, {\bf Z}_{t_0}) h(\Theta)

    associated to the process :math:`{\bf Z}_A`, where

    .. math::

       f(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i}) :=
          \pi({\bf Z}_{t_i} \vert {\bf Z}_{t_{i-1}}, \Theta) \,, \\
       g(\Theta, {\bf Z}_{t_0}) :=
          \pi({\bf Z}_{t_0} \vert \Theta) \; \text{and} \\
       h(\Theta) := \pi(\Theta)

    .. note:: The argument inputs are assumed in the order as above
       (i.e. :math:`\Theta, {\bf Z}_A`).
       The conditional distribution
       :math:`g(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i})`
       is assumed to be extending the class :class:`Distribution` and have the
       same interface, where the input :math:`{\bf x}` contains both
       :math:`\Theta, {\bf Z}_{t_{i-1}}` and :math:`{\bf Z}_{t_i}`.
       Each of the log-likelihoods already embed its own data :math:`{\bf y}_t`.
       The list of log-likelihoods must be of the same length of the list of
       transitions. Missing data are simulated by setting the corresponding
       entry in the list of log-likelihood to ``None``.

    Args:
      pi_list (:class:`list` of :class:`Distribution`): list of transition densities
        :math:`[g(\Theta, {\bf Z}_{t_0}), f(\Theta, {\bf Z}_{t_{0}}, {\bf Z}_{t_1}), \ldots ]`
      ll_list (:class:`list` of :class:`LogLikelihood<TransportMaps.Functionals.LogLikelihood>`):
        list of log-likelihoods
        :math:`\{\log\mathcal{L}({\bf y}_t \vert \Theta, {\bf Z}_t)\}_{t\in B}`
      pi_hyper (:class:`Distribution`): prior on hyper-parameters :math:`h(\Theta)`
    """
    def __init__(self, pi_list, ll_list, pi_hyper=None):
        super(SequentialHiddenMarkovChainDistribution, self).__init__(pi_list, pi_hyper)
        # Check consistency of likelihoods
        if len(pi_list) != len(ll_list):
            raise ValueError("Length of list of transition must be the same of " + \
                             "the list of log-likelihoods")
        for i, ll in enumerate(ll_list):
            if ll is not None and ll.dim != self.state_dim + self.hyper_dim:
                raise ValueError("Dimension of log-likelihood %d is not consistent" % i)
        # Init
        self.ll_list = ll_list

    def append(self, pi, ll=None):
        r""" Append a new transition distribution :math:`g(\Theta, {\bf Z}_{t_{k}}, {\bf Z}_{t_{k+1}})` and the corresponding log-likelihood :math:`\log\mathcal{L}({\bf y}_{t_k} \vert \Theta, {\bf Z}_{t_k})` if any.

        Args:
          pi (:class:`Distribution`): transition distribution
            :math:`g(\Theta, {\bf Z}_{t_{k}}, {\bf Z}_{t_{k+1}})`
          ll (:class:`LogLikelihood<TransportMaps.Functionals.LogLikelihood>`):
            log-likelihood
            :math:`\log\mathcal{L}({\bf y}_{t_k} \vert \Theta, {\bf Z}_{t_k})`.
            Missing data are represented by ``None``.
        """
        super(SequentialHiddenMarkovChainDistribution, self).append( pi )
        # Check consistency
        if ll is not None and ll.dim != self.state_dim + self.hyper_dim:
            raise ValueError("Dimension of log-likelihood is not consistent")
        # Append
        self.ll_list.append( ll )

    def get_MarkovComponent(self, i, n=1, state_map=None, hyper_map=None):
        r""" Extract the (:math:`n\geq 1` steps) :math:`i`-th Markov component from the distribution

        If :math:`i=0` the Markov component is given by

        .. math::

           \pi^{0:n}(\Theta, {\bf Z}_{t_0}, \ldots, {\bf Z}_{t_n}) :=
             \left( \prod_{t \in \{t_0,\ldots,t_n\} \cap B}
                \mathcal{L}({\bf y}_t \vert \Theta, {\bf Z}_t) \right)
             \left( \prod_{i=1}^n f(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i}) \right)
             g(\Theta, {\bf Z}_{t_0}) h(\Theta) \;.

        If :math:`i>0` then the Markov component is

        .. math::

           \pi^{i:i+n}\left(\Theta, {\bf Z}_{t_i}, \ldots, {\bf Z}_{t_{i+n}}\right) :=
             \eta(\Theta, {\bf Z}_{t_i}) 
             \left( \prod_{t \in \left\{t_{i+1},\ldots,t_{i+n}\right\} \cap B}
                \mathcal{L}\left({\bf y}_t \vert
                  \mathfrak{T}_{i-1}^{\Theta}(\Theta), {\bf Z}_t\right) \right)
             \left( \prod_{k=i+1}^{i+n-1}
                f\left(\mathfrak{T}_{i-1}^{\Theta}(\Theta),
                   {\bf Z}_{t_{k}}, {\bf Z}_{t_k+1}\right) \right)
             f\left(\mathfrak{T}_{i-1}^{\Theta}(\Theta),
               \mathfrak{M}_{i-1}^{1}(\Theta, {\bf Z}_{t_i}), {\bf Z}_{t_{i+1}}
             \right) \;,

        where :math:`\mathfrak{T}_{i-1}^{\Theta}` and
        :math:`\mathfrak{M}_{i-1}^{1}` are the hyper-parameter and forecast
        components of the map computed at step :math:`i-1`, using the
        sequential algorithm described in :cite:`Spantini2017`.

        Args:
          i (int): index :math:`i` of the Markov component
          n (int): number of steps :math:`n`
          state_map (:class:`TransportMap<TransportMaps.Maps.TransportMap>`):
            forecast map :math:`\mathfrak{M}_{i-1}^{1}` from step :math:`i-1`.
          hyper_map (:class:`TransportMap<TransportMaps.Maps.TransportMap>`):
            hyper-parameter map :math:`\mathfrak{T}_{i-1}^{\Theta}`
            from step :math:`i-1`.
        """
        if i == 0:
            out = MarkovComponentDistribution(
                i, self.pi_list[:n+1], self.ll_list[:n+1],
                self.state_dim, self.hyper_dim,
                self.pi_hyper)
        elif i > 0:
            out = MarkovComponentDistribution(
                i, self.pi_list[i+1:i+n+1], self.ll_list[i+1:i+n+1],
                self.state_dim, self.hyper_dim,
                self.pi_hyper,
                state_map, hyper_map)
        else:
            raise AttributeError("Index must be i >= 0")
        return out

    def log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" Evaluate :math:`\log \pi({\bf Z}_A, \Theta \vert {\bf y}_B)`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- values of
            :math:`\log \pi({\bf Z}_A, \Theta \vert {\bf y}_B)`
            at the ``x`` points.
        """
        out = super(SequentialHiddenMarkovChainDistribution, self).log_pdf(x, params, idxs_slice)
        # Add Likelihoods
        for i, ll in enumerate(self.ll_list):
            if ll is not None:
                start_state = self.hyper_dim + i * self.state_dim
                stop_state = start_state + self.state_dim
                xin = np.hstack( (x[:,:self.hyper_dim],
                                  x[:,start_state:stop_state]) )
                out += ll.evaluate( xin, params, idxs_slice )
        return out

    def grad_x_log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" Evaluate :math:`\nabla_{{\bf Z},\Theta} \log \pi({\bf Z}_A, \Theta \vert {\bf y}_B)`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- values of
            :math:`\nabla_{{\bf Z},\Theta} \log \pi({\bf Z}_A, \Theta \vert {\bf y}_B)`
            at the ``x`` points.
        """
        out = super(SequentialHiddenMarkovChainDistribution, self).grad_x_log_pdf(
            x, params, idxs_slice)
        # Add Likelihoods
        hdim = self.hyper_dim
        sdim = self.state_dim
        for i, ll in enumerate(self.ll_list):
            if ll is not None:
                s1 = hdim + i*sdim  # Start state
                s2 = s1 + sdim      # Stop state
                xin = np.hstack( (x[:,:hdim], x[:,s1:s2]) )
                gx = ll.grad_x( xin, params, idxs_slice )
                out[:,:hdim] += gx[:,:hdim]
                out[:,s1:s2] += gx[:,hdim:]
        return out

    def hess_x_log_pdf(self, x, params=None, idxs_slice=slice(None,None,None)):
        r""" Evaluate :math:`\nabla^2_{{\bf Z},\Theta} \log \pi({\bf Z}_A, \Theta \vert {\bf y}_B)`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          params (dict): parameters
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- values of
            :math:`\nabla^2_{{\bf Z},\Theta} \log \pi({\bf Z}_A, \Theta \vert {\bf y}_B)`
            at the ``x`` points.
        """
        out = super(SequentialHiddenMarkovChainDistribution, self).hess_x_log_pdf(
            x, params, idxs_slice)
        # Add Likelihoods
        hdim = self.hyper_dim
        sdim = self.state_dim
        for i, ll in enumerate(self.ll_list):
            if ll is not None:
                s1 = hdim + i*sdim  # Start state
                s2 = s1 + sdim      # Stop state
                xin = np.hstack( (x[:,:hdim], x[:,s1:s2]) )
                hx = ll.hess_x( xin, params, idxs_slice )
                out[:,:hdim,:hdim] += hx[:,:hdim,:hdim]
                out[:,:hdim,s1:s2] += hx[:,:hdim,hdim:]
                out[:,s1:s2,:hdim] += hx[:,hdim:,:hdim]
                out[:,s1:s2,s1:s2] += hx[:,hdim:,hdim:]
        return out
        
class MarkovComponentDistribution(Distribution):
    r""" :math:`i`-th Markov component of a :class:`SequentialHiddenMarkovChainDistribution`

    If :math:`i=0` the Markov component is given by

    .. math::

       \pi^{0:n}(\Theta, {\bf Z}_{t_0}, \ldots, {\bf Z}_{t_n}) :=
         \left( \prod_{t \in \{t_0,\ldots,t_n\} \cap B}
            \mathcal{L}({\bf y}_t \vert \Theta, {\bf Z}_t) \right)
         \left( \prod_{i=1}^n f(\Theta, {\bf Z}_{t_{i-1}}, {\bf Z}_{t_i}) \right)
         g(\Theta, {\bf Z}_{t_0}) h(\Theta) \;.

    If :math:`i>0` then the Markov component is

    .. math::

       \pi^{i:i+n}\left(\Theta, {\bf Z}_{t_i}, \ldots, {\bf Z}_{t_{i+n}}\right) :=
         \eta(\Theta, {\bf Z}_{t_i}) 
         \left( \prod_{t \in \left\{t_{i+1},\ldots,t_{i+n}\right\} \cap B}
            \mathcal{L}\left({\bf y}_t \vert
              \mathfrak{T}_{i-1}^{\Theta}(\Theta), {\bf Z}_t\right) \right)
         \left( \prod_{k=i+1}^{i+n-1}
            f\left(\mathfrak{T}_{i-1}^{\Theta}(\Theta),
               {\bf Z}_{t_{k}}, {\bf Z}_{t_k+1}\right) \right)
         f\left(\mathfrak{T}_{i-1}^{\Theta}(\Theta),
           \mathfrak{M}_{i-1}^{1}(\Theta, {\bf Z}_{t_i}), {\bf Z}_{t_{i+1}}
         \right) \;,

    where :math:`\mathfrak{T}_{i-1}^{\Theta}` and
    :math:`\mathfrak{M}_{i-1}^{1}` are the hyper-parameter and forecast
    components of the map computed at step :math:`i-1`, using the
    sequential algorithm described in :cite:`Spantini2017`.

    Args:
      idx0 (int): index :math:`i` of the Markov component
      pi_list (:class:`list` of :class:`Distribution`): list of :math:`n`
        transition densities
      ll_list (:class:`list` of :class:`LogLikelihood<TransportMaps.Functionals.LogLikelihood>`):
        list of :math:`n` log-likelihoods (``None`` for missing data)
        :math:`\{\log\mathcal{L}({\bf y}_t \vert \Theta, {\bf Z}_t)\}_{t\in B}`
      state_dim (int): dimension of the state-space
      hyper_dim (int): dimension of the parameter-space
      pi_hyper (:class:`Distribution`): prior on hyper-parameters :math:`h(\Theta)`
      state_map (:class:`TransportMap<TransportMaps.Maps.TransportMap>`):
        forecast map :math:`\mathfrak{M}_{i-1}^{1}` from step :math:`i-1`.
      hyper_map (:class:`TransportMap<TransportMaps.Maps.TransportMap>`):
        hyper-parameter map :math:`\mathfrak{T}_{i-1}^{\Theta}`
        from step :math:`i-1`.
    """
    def __init__(self, idx0, pi_list, ll_list,
                 state_dim, hyper_dim,
                 pi_hyper=None,
                 state_map=None, hyper_map=None):
        # Figure out dimension and check correct arguments are provided
        self.idx0 = idx0
        self.state_dim = state_dim
        self.hyper_dim = hyper_dim
        if idx0 == 0:
            if pi_hyper is not None and pi_hyper.dim != hyper_dim:
                raise AttributeError(
                    "Dimension of prior of hyper-paramenter not consistent")
            self.pi_hyper = pi_hyper
        elif idx0 > 0:
            if state_map is None:
                raise AttributeError(
                    "The state_map parameter must be provided for idx0>0")
            if state_map.dim_in != hyper_dim + state_dim:
                raise AttributeError(
                    "Dimension of state_map not consistent")
            if self.hyper_dim > 0 and hyper_map is None:
                raise AttributeError(
                    "The hyper_map parameter must be provided for hyper_dim>0")
            if self.hyper_dim > 0 and hyper_map.dim != hyper_dim:
                raise AttributeError(
                    "Dimension of hyper_map not consistent")
            self.state_map = state_map
            self.hyper_map = hyper_map
            self.pi_hyper = StandardNormalDistribution(hyper_dim + state_dim)
        else:
            raise AttributeError("Onli idx0>=0 admitted")
        if len(pi_list) != len(ll_list):
            raise AttributeError("Length of list of transition must be the same of " + \
                                 "the list of log-likelihoods")
        if idx0 == 0 and len(pi_list) < 2:
            raise AttributeError("The 0-th Markov component must be composed " + \
                                 "by at least two transition densities")
        if idx0 > 0 and len(pi_list) < 1:
            raise AttributeError("The (i>0)-th Markov component must be composed " + \
                                 "by at least one transition distribution")
        if idx0 == 0: # We can get away with a SequentialInferenceDistribution
            self.seqinfdens = SequentialHiddenMarkovChainDistribution(
                pi_list, ll_list, pi_hyper)
            dim = self.seqinfdens.dim
        else:
            dim = hyper_dim + state_dim
            for i, (pi, ll) in enumerate(zip(pi_list,ll_list)):
                if pi.dim != hyper_dim + 2*state_dim:
                    raise AttributeError(
                        "The dimension of the %d transition is not consistent" % i)
                if ll is not None and ll.dim != hyper_dim + state_dim:
                    raise AttributeError(
                        "The dimension of the %d log-likelihood is not consistent" % i)
                dim += state_dim
        self.pi_list = pi_list
        self.ll_list = ll_list
        super(MarkovComponentDistribution, self).__init__(dim)

    def log_pdf(self, x, *args, **kwargs):
        if self.idx0 == 0:
            out = self.seqinfdens.log_pdf(x, *args, **kwargs)
        else:
            xtr = x.copy() # Transformed
            hdim = self.hyper_dim
            sdim = self.state_dim
            # Apply hyper and component maps to obtain transformed inputs
            if hdim > 0:
                xtr[:,:hdim] = self.hyper_map.evaluate(x[:,:hdim], *args, **kwargs)
            xtr[:,hdim:hdim+sdim] = self.state_map.evaluate(
                x[:,:hdim+sdim], *args, **kwargs)
            # Evaluate pi_hyper
            out = self.pi_hyper.log_pdf(x[:,:hdim+sdim], *args, **kwargs)
            # Evaluate transitions and likelihoods
            for i, (pi, ll) in enumerate(zip(self.pi_list, self.ll_list)):
                s1 = hdim + i*sdim
                s2 = s1 + sdim
                s3 = s2 + sdim
                xin = np.hstack( (xtr[:,:hdim], xtr[:,s1:s3]) )
                out += pi.log_pdf(xin, *args, **kwargs)
                if ll is not None:
                    xin = np.hstack( (xtr[:,:hdim], xtr[:,s2:s3]) )
                    out += ll.evaluate(xin, *args, **kwargs)
        return out

    def grad_x_log_pdf(self, x, *args, **kwargs):
        if self.idx0 == 0:
            out = self.seqinfdens.grad_x_log_pdf(x, *args, **kwargs)
        else:
            xtr = x.copy() # Transformed input
            hdim = self.hyper_dim
            sdim = self.state_dim
            # Apply hyper and component maps to obtain transformed inputs and
            # compute gradients of the maps
            if hdim > 0:
                xtr[:,:hdim] = self.hyper_map.evaluate(x[:,:hdim], *args, **kwargs)
                gx_hyper = self.hyper_map.grad_x(x[:,:hdim], *args, **kwargs)
            xtr[:,hdim:hdim+sdim] = self.state_map.evaluate(
                x[:,:hdim+sdim], *args, **kwargs)
            gx_comp = self.state_map.grad_x(x[:,:hdim+sdim], *args, **kwargs)
            # Evaluate
            out = np.zeros((x.shape[0], self.dim))
            # Evaluate pi_hyper
            out[:,:hdim+sdim] += self.pi_hyper.grad_x_log_pdf(
                x[:,:hdim+sdim], *args, **kwargs)
            # Evaluate transitions and likelihoods
            for i, (pi, ll) in enumerate(zip(self.pi_list, self.ll_list)):
                s1 = hdim + i*sdim
                s2 = s1 + sdim
                s3 = s2 + sdim
                xin = np.hstack( (xtr[:,:hdim], xtr[:,s1:s3]) )
                # Transition
                gxlpdf = pi.grad_x_log_pdf(xin, *args, **kwargs)
                gxlpdfinner = np.zeros(gxlpdf.shape)
                gxlpdfinner[:,hdim+sdim:] = gxlpdf[:,hdim+sdim:]
                if hdim > 0: # Apply gradient hyper map
                    gxlpdfinner[:,:hdim] += np.einsum(
                        '...i,...ij->...j', gxlpdf[:,:hdim], gx_hyper)
                if i == 0: # Apply gradient component map
                    gxlpdfinner[:,:hdim+sdim] += np.einsum(
                        '...i,...ij->...j', gxlpdf[:,hdim:hdim+sdim], gx_comp)
                else:
                    gxlpdfinner[:,hdim:sdim] = gxlpdf[:,hdim:sdim]
                out[:,:hdim] += gxlpdfinner[:,:hdim]
                out[:,s1:s3] += gxlpdfinner[:,hdim:]
                # Likelihood
                if ll is not None:
                    xin = np.hstack( (xtr[:,:hdim], xtr[:,s2:s3]) )
                    gxll = ll.grad_x(xin, *args, **kwargs)
                    if hdim > 0:
                        gxll[:,:hdim] = np.einsum(
                            '...i,...ij->...j', gxll[:,:hdim], gx_hyper)
                    out[:,:hdim] += gxll[:,:hdim]
                    out[:,s2:s3] += gxll[:,hdim:]
        return out

    def hess_x_log_pdf(self, x, *args, **kwargs):
        if self.idx0 == 0:
            out = self.seqinfdens.hess_x_log_pdf(x, *args, **kwargs)
        else:
            xtr = x.copy() # Transformed input
            hdim = self.hyper_dim
            sdim = self.state_dim
            # Apply hyper and component maps to obtain transformed inputs and
            # compute gradients and Hessians of the maps
            xtr[:,hdim:hdim+sdim] = self.state_map.evaluate(
                x[:,:hdim+sdim], *args, **kwargs)
            gx_comp = self.state_map.grad_x(x[:,:hdim+sdim], *args, **kwargs)
            gx2_comp = gx_comp[:,:,:,nax,nax] * gx_comp[:,nax,nax,:,:]
            hx_comp = self.state_map.hess_x(x[:,:hdim+sdim], *args, **kwargs)
            if hdim > 0:
                xtr[:,:hdim] = self.hyper_map.evaluate(x[:,:hdim], *args, **kwargs)
                gx_hyper = self.hyper_map.grad_x(x[:,:hdim], *args, **kwargs)
                gx2_hyper = gx_hyper[:,:,:,nax,nax] * gx_hyper[:,nax,nax,:,:]
                hx_hyper = self.hyper_map.hess_x(x[:,:hdim], *args, **kwargs)
                # Cross term
                gx2_hyper_comp = gx_hyper[:,:,:,nax,nax] * gx_comp[:,nax,nax,:,:]
            # Evaluate
            out = np.zeros((x.shape[0], self.dim, self.dim))
            # Evaluate pi_hyper
            out[:,:hdim+sdim,:hdim+sdim] += self.pi_hyper.hess_x_log_pdf(
                x[:,:hdim+sdim], *args, **kwargs)
            # Evaluate transitions and likelihoods
            for i, (pi, ll) in enumerate(zip(self.pi_list, self.ll_list)):
                s1 = hdim + i*sdim
                s2 = s1 + sdim
                s3 = s2 + sdim
                xin = np.hstack( (xtr[:,:hdim], xtr[:,s1:s3]) )
                #############
                # Transition
                c1 = hdim
                c2 = c1 + sdim
                hxlpdf = pi.hess_x_log_pdf(xin, *args, **kwargs)
                gxlpdf = pi.grad_x_log_pdf(xin, *args, **kwargs)
                hx = np.zeros(hxlpdf.shape)
                hx[:,c2:,c2:] = hxlpdf[:,c2:,c2:] # Identity
                gx = np.zeros(hxlpdf.shape)
                if hdim > 0: # Apply hyper map
                    hx[:,:c1,:c1] += np.einsum(
                        '...ij,...ikjl->...kl', hxlpdf[:,:c1,:c1], gx2_hyper)
                    hx[:,:c1,c2:] += np.einsum(
                        '...ij,...ik->...kj', hxlpdf[:,:c1,c2:], gx_hyper)
                    gx[:,:c1,:c1] += np.einsum(
                        '...i,...ijk->...jk', gxlpdf[:,:c1], hx_hyper)
                if i == 0: # Apply component map
                    hx[:,:c2,:c2] += np.einsum(
                        '...ij,...ikjl->...kl', hxlpdf[:,c1:c2,c1:c2], gx2_comp)
                    hx[:,:c2,c2:] += np.einsum(
                        '...ij,...ik->...kj', hxlpdf[:,c1:c2,c2:], gx_comp)
                    gx[:,:c2,:c2] += np.einsum(
                        '...i,...ijk->...jk', gxlpdf[:,:c2], hx_comp)
                    if hdim > 0: # Apply cross term
                        tmp = np.einsum(
                            '...ij,...ikjl->...kl', hxlpdf[:,:hdim,c1:c2], gx2_hyper_comp)
                        hx[:,:hdim,:c2] += tmp
                        hx[:,:c2,:hdim] += tmp.transpose((0,2,1))
                else:
                    hx[:,c1:c2,c1:c2] = hxlpdf[:,c1:c2,c1:c2]
                    hx[:,c1:c2,c2:] = hxlpdf[:,c1:c2,c2:]
                # Symmetrize hx
                hx[:,c1:,:c1] = hx[:,:c1,c1:].transpose((0,2,1))
                hx[:,c2:,c1:c2] = hx[:,c1:c2,c2:].transpose((0,2,1))
                # Update out
                out[:,:hdim,:hdim] += hx[:,:hdim,:hdim] + gx[:,:hdim,:hdim]
                out[:,:hdim,s1:s3] += hx[:,:hdim,hdim:] + gx[:,:hdim,hdim:]
                out[:,s1:s3,:hdim] += hx[:,hdim:,:hdim] + gx[:,hdim:,:hdim]
                out[:,s1:s3,s1:s3] += hx[:,hdim:,hdim:] + gx[:,hdim:,hdim:]
                #############
                # Likelihood
                if ll is not None:
                    xin = np.hstack( (xtr[:,:hdim], xtr[:,s2:s3]) )
                    hxll = ll.hess_x(xin, *args, **kwargs)
                    gxll = ll.grad_x(xin, *args, **kwargs)
                    gx = np.zeros(hxll.shape)
                    if hdim > 0:
                        hxll[:,:hdim,:hdim] = np.einsum(
                            '...ij,...ikjl->...kl', hxll[:,:hdim,:hdim], gx2_hyper)
                        gx[:,:hdim,:hdim] = np.einsum(
                            '...i,...ijk->...jk', gxll[:,:hdim], hx_hyper)
                    out[:,:hdim,:hdim] += hxll[:,:hdim,:hdim] + gx[:,:hdim,:hdim]
                    out[:,:hdim,s2:s3] += hxll[:,:hdim,hdim:]
                    out[:,s2:s3,:hdim] += hxll[:,hdim:,:hdim]
                    out[:,s2:s3,s2:s3] += hxll[:,hdim:,hdim:]
        return out