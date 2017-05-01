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
import numpy as np
import numpy.linalg as npla
import scipy.stats as stats
import scipy.linalg as scila

import SpectralToolbox.Spectral1D as S1D
import SpectralToolbox.SpectralND as SND

from TransportMaps.Distributions.DistributionBase import *
from TransportMaps.Distributions.TransportMapDistributions import *

__all__ = ['FrozenDistribution_1d',
           'GaussianDistribution', 'StandardNormalDistribution',
           'LogNormalDistribution', 'LogisticDistribution',
           'GammaDistribution', 'BetaDistribution',
           'WeibullDistribution',
           'GumbelDistribution', 'BananaDistribution']

nax = np.newaxis

class FrozenDistribution_1d(Distribution):
    r""" [Abstract] Generic frozen distribution 1d
    """
    def __init__(self):
        super(FrozenDistribution_1d,self).__init__(1)
        self.base = StandardNormalDistribution(1)
        self.scipy_base = stats.norm()
    def rvs(self, n, *args, **kwargs):
        return self.dist.rvs(n).reshape((n,1))
    def quadrature(self, qtype, qparams, *args, **kwargs):
        r""" Generate quadrature points and weights.

        Types of quadratures:

        Monte-Carlo (``qtype==0``)
           ``qparams``: (:class:`int`) -- number of samples

        Quasi-Monte-Carlo (``qtype==1``)
           ``qparams``: (:class:`int`) -- number of samples

        Latin-Hypercube-Sampling (``qtype==2``)
           ``qparams``: (:class:`int`) -- number of samples

        Gauss-quadrature (``qtype==3``)
           ``qparams``: (:class:`list<list>` [:math:`d`]) -- orders for
           each dimension

        .. seealso:: :func:`Distribution.quadrature`
        """
        if qtype == 0:
            # Monte Carlo sampling
            x = self.rvs(qparams)
            w = np.ones(qparams)/float(qparams)
        elif qtype == 1:
            # Quasi-Monte Carlo sampling
            raise NotImplementedError("Not implemented")
        elif qtype == 2:
            # Latin-Hyper cube sampling
            raise NotImplementedError("Todo")
        elif qtype == 3:
            # Gaussian quadrature
            (x1,w) = self.base.quadrature(3, qparams)
            x = self.dist.ppf( self.scipy_base.cdf(x1[:,0]) )[:,nax]
        else:
            raise ValueError("Quadrature type not recognized")
        return (x,w)

#########################################################
# Definitions of Gaussian and Standard normal densities #
#########################################################
class GaussianDistribution(Distribution):
    r""" Multivariate Gaussian distribution :math:`\pi`

    Args:
      mu (:class:`ndarray<numpy.ndarray>` [:math:`d`]): mean vector
      sigma (:class:`ndarray<numpy.ndarray>` [:math:`d,d`]): covariance matrix
      precision (:class:`ndarray<numpy.ndarray>` [:math:`d,d`]): precision matrix
    """

    def __init__(self, mu, sigma=None, precision=None):
        if (sigma is not None) and (precision is not None):
            raise ValueError("The fields sigma and precision are mutually " +
                             "exclusive")
        if sigma is not None:
            if mu.shape[0] != sigma.shape[0] or mu.shape[0] != sigma.shape[1]:
                raise ValueError("Dimension d of mu and sigma must be the same")
        if precision is not None:
            if mu.shape[0] != precision.shape[0] or mu.shape[0] != precision.shape[1]:
                raise ValueError("Dimension d of mu and precision must be the same")
        super(GaussianDistribution,self).__init__(mu.shape[0])
        self.mu = mu
        if sigma is not None:
            self.sigma = sigma
            try:
                chol = scila.cho_factor(self.sigma, True) # True: lower triangular
            except scila.LinAlgError:
                # Add little diagonal term
                sig_infl = self.sigma + np.diag(np.ones(self.dim))*1e-13
                chol = scila.cho_factor(sig_infl, True)
                self.logger.warning(
                    "Covariance matrix has been lifted to make it positive definite")
                # # Obtain the square root from svd
                # u,s,v = scila.svd(self.sigma)
                # self.log_det_sigma = np.sum(np.log(s))
                # self.det_sigma = np.exp( self.log_det_sigma )
                # self.sampling_mat = u * np.sqrt(s)[np.newaxis,:]
                # self.inv_sigma = np.dot(u * (1./s)[np.newaxis,:], v.T)
            finally:
                self.det_sigma = np.prod(np.diag(chol[0]))**2.
                self.log_det_sigma = 2. * np.sum( np.log( np.diag(chol[0]) ) )
                self.sampling_mat = np.tril(chol[0])
                self.inv_sigma = scila.cho_solve(chol, np.eye(self.dim))
        if precision is not None:
            self.inv_sigma = precision
            chol = scila.cho_factor(self.inv_sigma, False) # False: upper triangular
            self.det_sigma = 1. / np.prod(np.diag(chol[0]))**2.
            self.log_det_sigma = - 2. * np.sum( np.log( np.diag(chol[0]) ) )
            self.sampling_mat = scila.solve_triangular(np.triu(chol[0]),
                                                       np.eye(self.dim),
                                                       lower=False)
        self.norm = stats.norm()

    def rvs(self, m, *args, **kwargs):
        r""" Generate :math:`m` samples from the distribution.

        Args:
          m (int): number of samples

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- samples

        .. seealso:: :func:`Distribution.rvs`
        """
        z = self.norm.rvs(m*self.dim).reshape((m,self.dim))
        samples = self.mu + np.dot( self.sampling_mat, z.T ).T
        return samples

    def quadrature(self, qtype, qparams, *args, **kwargs):
        r""" Generate quadrature points and weights.

        Types of quadratures:

        Monte-Carlo (``qtype==0``)
           ``qparams``: (:class:`int`) -- number of samples

        Quasi-Monte-Carlo (``qtype==1``)
           ``qparams``: (:class:`int`) -- number of samples

        Latin-Hypercube-Sampling (``qtype==2``)
           ``qparams``: (:class:`int`) -- number of samples

        Gauss-quadrature (``qtype==3``)
           ``qparams``: (:class:`list<list>` [:math:`d`]) -- orders for
           each dimension

        .. seealso:: :func:`Distribution.quadrature`
        """
        if qtype == 0:
            # Monte Carlo sampling
            x = self.rvs(qparams)
            w = np.ones(qparams)/float(qparams)
        elif qtype == 1:
            # Quasi-Monte Carlo sampling
            raise NotImplementedError("Not implemented")
        elif qtype == 2:
            # Latin-Hyper cube sampling
            raise NotImplementedError("Todo")
        elif qtype == 3:
            # Gaussian quadrature
            # Generate first a standard normal quadrature
            # then apply the Cholesky transform
            P = SND.PolyND( [S1D.HermiteProbabilistsPolynomial()] * self.dim )
            (x,w) = P.GaussQuadrature(qparams)
            x = np.dot( self.sampling_mat, x.T ).T
            x += self.mu
        else:
            raise ValueError("Quadrature type not recognized")
        return (x,w)

    def pdf(self, x, *args, **kwargs):
        r""" Evaluate :math:`\pi(x)`

        .. seealso:: :func:`Distribution.pdf`
        """
        return np.exp( self.log_pdf(x) )

    def log_pdf(self, x, *args, **kwargs):
        r""" Evaluate :math:`\log\pi(x)`

        .. seealso:: :func:`Distribution.log_pdf`
        """
        b = x - self.mu
        sol = np.dot( self.inv_sigma, b.T ).T
        out = - .5 * np.einsum('...i,...i->...', b, sol) \
              - self.dim * .5 * np.log(2.*np.pi) \
              - .5 * self.log_det_sigma
        return out.flatten()

    def grad_x_log_pdf(self, x, *args, **kwargs):
        r""" Evaluate :math:`\nabla_{\bf x}\log\pi(x)`

        .. seealso:: :func:`Distribution.grad_x_log_pdf`
        """
        b = x - self.mu
        return - np.dot( self.inv_sigma, b.T ).T

    def hess_x_log_pdf(self, x, *args, **kwargs):
        r""" Evaluate :math:`\nabla^2_{\bf x}\log\pi(x)`

        .. seealso:: :func:`Distribution.hess_x_log_pdf`
        """
        return - np.ones(x.shape[0])[:,nax,nax] * self.inv_sigma[nax,:,:]

    def mean_log_pdf(self):
        r""" Evaluate :math:`\mathbb{E}_{\pi}[\log \pi]`.

        .. seealso:: :func:`Distribution.mean_log_pdf`
        """
        return - .5 * ( self.dim * np.log(2*np.pi) + self.dim + self.log_det_sigma )

class StandardNormalDistribution(GaussianDistribution):
    r""" Multivariate Standard Normal distribution :math:`\pi`.

    Args:
      d (int): dimension
    """

    def __init__(self, dim):
        mu = np.zeros(dim)
        sig = np.eye(dim)
        super(StandardNormalDistribution,self).__init__(mu,sig)

    def rvs(self, m, *args, **kwargs):
        r""" Generate :math:`m` samples from the distribution.

        Args:
          m (int): number of samples

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- samples

        .. seealso:: :func:`Distribution.rvs`
        """
        return self.norm.rvs(m*self.dim).reshape((m,self.dim))


###############################################################
# Definition of miscellaneous densities (No sampling defined) #
###############################################################
class LogNormalDistribution(FrozenDistribution_1d):
    def __init__(self, s, mu, scale):
        super(LogNormalDistribution,self).__init__()
        self.s = s
        self.mu = mu
        self.scale = scale
        self.dist = stats.lognorm(s=s,
                                  loc=mu,
                                  scale=scale)
    def rvs(self, n, *args, **kwargs):
        return self.dist.rvs(n).reshape((n,1))
    def pdf(self, x, *args, **kwargs):
        return self.dist.pdf( x ).flatten()
    def grad_x_pdf(self, x, *args, **kwargs):
        s = self.s
        m = self.mu
        d = self.dist
        return - d.pdf(x) * ( 1./(x-m) + np.log(x-m)/(s**2.*(x-m)) )
    def log_pdf(self, x, *args, **kwargs):
        return self.dist.logpdf( x ).flatten()
    def grad_x_log_pdf(self, x, *args, **kwargs):
        s = self.s
        m = self.mu
        sc = self.scale
        return - 1./(x-m) * (np.log((x-m)/sc)/s**2. + 1)
    def hess_x_log_pdf(self, x, *args, **kwargs):
        s = self.s
        m = self.mu
        sc = self.scale
        return (1./(x-m)**2. * ( (np.log((x-m)/sc) + s**2. - 1.)/s**2. ))[:,:,nax]

class LogisticDistribution(FrozenDistribution_1d):
    def __init__(self, mu, s):
        super(LogisticDistribution,self).__init__()
        self.mu = mu
        self.s = s
        self.dist = stats.logistic(loc=mu,scale=s)
    def rvs(self, n, *args, **kwargs):
        return self.dist.rvs(n).reshape((n,1))
    def pdf(self, x, *args, **kwargs):
        return self.dist.pdf(x).flatten()
    def log_pdf(self, x, *args, **kwargs):
        # Log pdf with modified asymptotic behavior
        out = np.zeros(x.shape)
        g20 = (x >= -20)
        l20 = (x < -20)
        out[g20] = self.dist.logpdf(x[g20]).flatten()
        out[l20] = (x[l20].flatten() - self.mu)/self.s
        return out.flatten()
    def grad_x_log_pdf(self, x, *args, **kwargs):
        mu = self.mu
        s = self.s
        out = np.zeros(x.shape)
        g20 = (x >= -20)
        l20 = (x < -20)
        g = np.exp(-(x[g20]-mu)/s)
        out[g20] = -1./s + 2./s * g/(1+g)
        out[l20] = 1./s
        return out
    def hess_x_log_pdf(self, x, *args, **kwargs):
        mu = self.mu
        s = self.s
        out = np.zeros(x.shape)
        g20 = (x >= -20)
        l20 = (x < -20)
        g = np.exp(-(x[g20]-mu)/s)
        out[g20] = (- 2./s**2. * g/(1+g)**2.)
        out[l20] = 0.
        return out[:,:,nax]
    # def nabla3_x_log_pdf(self, x, params=None):
    #     mu = self.mu
    #     s = self.s
    #     g = np.exp(-(x-mu)/s)
    #     return (2./s**3. * g*(1-g)/(1+g)**3.)[:,:,nax,nax]

class GammaDistribution(FrozenDistribution_1d):
    def __init__(self, kappa, theta):
        super(GammaDistribution,self).__init__()
        self.kappa = kappa
        self.theta = theta
        self.dist = stats.gamma(kappa, scale=theta)
    def rvs(self, n, *args, **kwargs):
        return self.dist.rvs(n).reshape((n,1))
    def pdf(self, x, *args, **kwargs):
        return self.dist.pdf(x).flatten()
    def log_pdf(self, x, *args, **kwargs):
        return self.dist.logpdf(x).flatten()
    def grad_x_log_pdf(self, x, *args, **kwargs):
        k = self.kappa
        t = self.theta
        return (k-1.)/x - 1/t
    def hess_x_log_pdf(self, x, *args, **kwargs):
        k = self.kappa
        return ((1.-k)/x**2.)[:,:,nax]
    def nabla3_x_log_pdf(self, x, *args, **kwargs):
        k = self.kappa
        return (2.*(k-1.)/x**3.)[:,:,nax,nax]

class BetaDistribution(FrozenDistribution_1d):
    def __init__(self, alpha, beta):
        super(BetaDistribution,self).__init__()
        self.alpha = alpha
        self.beta = beta
        self.dist = stats.beta(alpha, beta)
    def rvs(self, n, *args, **kwargs):
        return self.dist.rvs(n).reshape((n,1))
    def pdf(self, x, *args, **kwargs):
        return self.dist.pdf(x).flatten()
    def log_pdf(self, x, *args, **kwargs):
        return self.dist.logpdf(x).flatten()
    def grad_x_log_pdf(self, x, *args, **kwargs):
        a = self.alpha
        b = self.beta
        return (a-1.)/x + (b-1.)/(x-1.)
    def hess_x_log_pdf(self, x, *args, **kwargs):
        a = self.alpha
        b = self.beta
        out = (1.-a)/x**2. + (1-b)/(x-1.)**2.
        return out[:,:,nax]
    def nabla3_x_log_pdf(self, x, *args, **kwargs):
        a = self.alpha
        b = self.beta
        out = 2.*(a-1.)/x**3. + 2.*(b-1.)/(x-1.)**3.
        return out[:,:,nax,nax]

class GumbelDistribution(FrozenDistribution_1d):
    def __init__(self, mu, beta):
        super(GumbelDistribution,self).__init__()
        self.mu = mu
        self.beta = beta
        self.dist = stats.gumbel_r(loc=mu, scale=beta)
    def rvs(self, n, *args, **kwargs):
        return self.dist.rvs(n).reshape((n,1))
    def pdf(self, x, *args, **kwargs):
        return self.dist.pdf(x).flatten()
    def log_pdf(self, x, *args, **kwargs):
        return self.dist.logpdf(x).flatten()
    def grad_x_log_pdf(self, x, *args, **kwargs):
        m = self.mu
        b = self.beta
        z = (x-m)/b
        return (np.exp(-z)-1.)/b
    def hess_x_log_pdf(self, x, *args, **kwargs):
        m = self.mu
        b = self.beta
        z = (x-m)/b
        return (- np.exp(-z)/b**2.)[:,:,nax]
    def nabla3_x_log_pdf(self, x, *args, **kwargs):
        m = self.mu
        b = self.beta
        z = (x-m)/b
        return (np.exp(-z)/b**3.)[:,:,nax,nax]

class WeibullDistribution(FrozenDistribution_1d):
    def __init__(self, c, mu=0., sigma=1.):
        super(WeibullDistribution,self).__init__()
        self.c = c
        self.mu = mu
        self.sigma=sigma
        self.dist = stats.weibull_min(c=self.c, loc=self.mu, scale=self.sigma)
    def rvs(self, n, *args, **kwargs):
        return self.dist.rvs(n).reshape((n,1))
    def pdf(self, x, *args, **kwargs):
        return self.dist.pdf(x).flatten()
    def log_pdf(self, x, *args, **kwargs):
        return self.dist.logpdf(x).flatten()
    def grad_x_log_pdf(self, x, *args, **kwargs):
        c = self.c
        m = self.mu
        s = self.sigma
        out = (c-1.)/(x-m) - c/s * ((x-m)/s)**(c-1.)
        return out
    def hess_x_log_pdf(self, x, *args, **kwargs):
        c = self.c
        m = self.mu
        s = self.sigma
        out = - (c-1.)/(x-m)**2. - (c*(c-1.))/s**2. * ((x-m)/s)**(c-2.)
        return out[:,:,nax]

class BananaDistribution(PushForwardTransportMapDistribution):
    def __init__(self, a, b, mu, sigma2):
        import TransportMaps.Maps as MAPS
        gauss_map = MAPS.LinearTransportMap( mu, npla.cholesky(sigma2) )
        ban_map = MAPS.FrozenBananaTransportMap(a, b)
        tm = MAPS.CompositeTransportMap(ban_map, gauss_map)
        base_distribution = StandardNormalDistribution(2)
        super(BananaDistribution, self).__init__(tm, base_distribution)
