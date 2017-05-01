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

import unittest
import numpy as np
import numpy.random as npr
npr.seed(1)
import numpy.linalg as npla
from scipy import stats

import TransportMaps.Distributions as DIST
from TransportMaps import FiniteDifference as FD

try:
    import mpi_map
    MPI_SUPPORT = True
except:
    MPI_SUPPORT = False

class DistributionTest(unittest.TestCase):

    def setUp(self):
        # Defined in subclasses
        self.d = self.get_d()
        self.distribution = self.get_distribution()
        self.integ = self.get_analytic_integral()
        self.f = self.get_test_function()
        self.mc_eps = self.get_mc_eps()
        self.quad_eps = self.get_quad_eps()

    def get_d(self):
        raise NotImplementedError("Define the dimension in sub-class")

    def get_distribution(self):
        raise NotImplementedError("Define the distribution in sub-class")

    def get_analytic_integral(self):
        r""" Value :math:`\mathbb{E}_\pi[x]`
        """
        raise NotImplementedError("Define the analytic integral with respect " +
                                  "to the distribution sub-class")

    def get_test_function(self):
        raise NotImplementedError("Define the test function in sub-class")

    def get_mc_eps(self):
        raise NotImplementedError("Define eps for mc test in sub-class")

    def get_quad_eps(self):
        raise NotImplementedError("Define eps for quadrature tests in sub-class")

    def test_rvs(self):
        n = 100
        ninc = 5
        success = False
        nit = 0
        while not success and nit < ninc:
            n *= 10
            x = self.distribution.rvs(n)
            intapp = np.sum(self.f(x))/float(n)
            success = np.isclose(intapp,self.integ,atol=self.mc_eps)
            nit += 1
        self.assertTrue(success)

    def test_log_pdf(self):
        n = 100
        x = self.distribution.rvs(n)
        pdf = self.distribution.pdf(x)
        log_pdf = self.distribution.log_pdf(x)
        self.assertTrue( np.allclose( np.log(pdf), log_pdf ) )

    def test_grad_x_log_pdf(self):
        n = 100
        dx = 1e-5
        x = self.distribution.rvs(n)
        gxlp_exa = self.distribution.grad_x_log_pdf(x)
        gxlp_fd = FD.grad_x_fd(self.distribution.log_pdf, x, dx, None)
        self.assertTrue( np.allclose(gxlp_fd, gxlp_exa, dx) )

    def test_hess_x_log_pdf(self):
        n = 100
        dx = 1e-5
        x = self.distribution.rvs(n)
        hxlp_exa = self.distribution.hess_x_log_pdf(x)
        hxlp_fd = FD.grad_x_fd(self.distribution.grad_x_log_pdf, x, dx, None)
        self.assertTrue( np.allclose(hxlp_fd, hxlp_exa, dx) )

    def test_mean_log_pdf(self):
        n = 100
        ninc = 5
        success = False
        nit = 0
        while not success and nit < ninc:
            n *= 10
            x = self.distribution.rvs(n)
            samps = self.distribution.log_pdf(x)
            intapp = np.sum(samps)/float(n)
            success = np.isclose(intapp, self.distribution.mean_log_pdf(),
                                 atol=self.mc_eps)
            nit += 1
        self.assertTrue(success)

class GaussianDistributionSigmaTests(DistributionTest):

    def get_distribution(self):
        mu = stats.norm().rvs(self.d)
        S = stats.norm().rvs(self.d**2).reshape((self.d,self.d))
        sig = np.dot(S.T, S)
        return DIST.GaussianDistribution(mu, sig)    

    def get_d(self):
        return 5

    def get_test_function(self):
        f = lambda x: np.sum(x, axis=0)
        return f

    def get_analytic_integral(self):
        return np.sum(self.distribution.mu)

    def get_mc_eps(self):
        return 1e-2

    def get_quad_eps(self):
        return 1e-10

    def test_gauss_quadrature(self):
        order = 1
        success = 0
        maxord = 20
        while not success and order <= maxord:
            (x,w) = self.distribution.quadrature(3, [order]*self.d)
            intapp = np.dot(self.f(x.T), w)
            success = np.isclose(intapp,self.integ,atol=self.quad_eps)
            order += 1
        self.assertTrue(success)

class GaussianDistributionPrecisionTests(DistributionTest):

    def get_distribution(self):
        mu = stats.norm().rvs(self.d)
        S = stats.norm().rvs(self.d**2).reshape((self.d,self.d))
        sig = np.dot(S.T, S)
        prec = npla.solve(sig, np.eye(self.d))
        return DIST.GaussianDistribution(mu, precision=prec)    

    def get_d(self):
        return 5

    def get_test_function(self):
        f = lambda x: np.sum(x, axis=0)
        return f

    def get_analytic_integral(self):
        return np.sum(self.distribution.mu)

    def get_mc_eps(self):
        return 1e-2

    def get_quad_eps(self):
        return 1e-10

    def test_gauss_quadrature(self):
        order = 1
        success = 0
        maxord = 20
        while not success and order <= maxord:
            (x,w) = self.distribution.quadrature(3, [order]*self.d)
            intapp = np.dot(self.f(x.T), w)
            success = np.isclose(intapp,self.integ,atol=self.quad_eps)
            order += 1
        self.assertTrue(success)


class StandardNormalDistributionTest(GaussianDistributionSigmaTests):

    def get_distribution(self):
        return DIST.StandardNormalDistribution(self.d)

class LogNormalDistributionTest(DistributionTest):
    def get_distribution(self):
        return DIST.LogNormalDistribution(.3,0.,2.)
    def get_d(self): return 1
    def get_analytic_integral(self): return None
    def get_test_function(self): return None
    def get_mc_eps(self): return None
    def get_quad_eps(self): return None
    @unittest.skip("Not defined")
    def test_rvs(self): pass
    @unittest.skip("Not defined")
    def test_mean_log_pdf(self): pass

class LogisticDistributionTest(DistributionTest):
    def get_distribution(self):
        return DIST.LogisticDistribution(1.,1.5)
    def get_d(self): return 1
    def get_analytic_integral(self): return None
    def get_test_function(self): return None
    def get_mc_eps(self): return None
    def get_quad_eps(self): return None
    @unittest.skip("Not defined")
    def test_rvs(self): pass
    @unittest.skip("Not defined")
    def test_mean_log_pdf(self): pass

class GammaDistributionTest(DistributionTest):
    def get_distribution(self):
        return DIST.GammaDistribution(2.,5.)
    def get_d(self): return 1
    def get_analytic_integral(self): return None
    def get_test_function(self): return None
    def get_mc_eps(self): return None
    def get_quad_eps(self): return None
    @unittest.skip("Not defined")
    def test_rvs(self): pass
    @unittest.skip("Not defined")
    def test_mean_log_pdf(self): pass

class BetaDistributionTest(DistributionTest):
    def get_distribution(self):
        return DIST.BetaDistribution(2.,5.)
    def get_d(self): return 1
    def get_analytic_integral(self): return None
    def get_test_function(self): return None
    def get_mc_eps(self): return None
    def get_quad_eps(self): return None
    @unittest.skip("Not defined")
    def test_rvs(self): pass
    @unittest.skip("Not defined")
    def test_mean_log_pdf(self): pass

class GumbelDistributionTest(DistributionTest):
    def get_distribution(self):
        return DIST.GumbelDistribution(2.,5.)
    def get_d(self): return 1
    def get_analytic_integral(self): return None
    def get_test_function(self): return None
    def get_mc_eps(self): return None
    def get_quad_eps(self): return None
    @unittest.skip("Not defined")
    def test_rvs(self): pass
    @unittest.skip("Not defined")
    def test_mean_log_pdf(self): pass

class WeibullDistributionTest(DistributionTest):
    def get_distribution(self):
        return DIST.WeibullDistribution(2.,2.,2.)
    def get_d(self): return 1
    def get_analytic_integral(self): return None
    def get_test_function(self): return None
    def get_mc_eps(self): return None
    def get_quad_eps(self): return None
    @unittest.skip("Not defined")
    def test_rvs(self): pass
    @unittest.skip("Not defined")
    def test_mean_log_pdf(self): pass

class BananaDistributionTest(DistributionTest):
    def get_distribution(self):
        return DIST.BananaDistribution(a=2.,b=2.,mu=np.zeros(2),sigma2=np.eye(2))
    def get_d(self): return 2
    def get_analytic_integral(self): return None
    def get_test_function(self): return None
    def get_mc_eps(self): return None
    def get_quad_eps(self): return None
    @unittest.skip("Not defined")
    def test_rvs(self): pass
    @unittest.skip("Not defined")
    def test_mean_log_pdf(self): pass

def build_suite(ttype='all'):
    suite_stdnorm = unittest.TestLoader().loadTestsFromTestCase( StandardNormalDistributionTest )
    suite_gaussian_sigma = unittest.TestLoader().loadTestsFromTestCase( GaussianDistributionSigmaTests )
    suite_gaussian_precision = unittest.TestLoader().loadTestsFromTestCase( GaussianDistributionPrecisionTests )
    suite_lognormal = unittest.TestLoader().loadTestsFromTestCase( LogNormalDistributionTest )
    suite_logistic = unittest.TestLoader().loadTestsFromTestCase( LogisticDistributionTest )
    suite_gamma = unittest.TestLoader().loadTestsFromTestCase( GammaDistributionTest )
    suite_beta = unittest.TestLoader().loadTestsFromTestCase( BetaDistributionTest )
    suite_gumbel = unittest.TestLoader().loadTestsFromTestCase( GumbelDistributionTest )
    suite_weibull = unittest.TestLoader().loadTestsFromTestCase( WeibullDistributionTest )
    suite_banana = unittest.TestLoader().loadTestsFromTestCase( BananaDistributionTest )
    # Group suites
    suites_list = []
    if ttype in ['all', 'serial']:
        suites_list += [ suite_stdnorm, suite_gaussian_sigma,
                         suite_gaussian_precision,
                         suite_lognormal, suite_logistic, suite_gamma, suite_beta,
                         suite_gumbel, suite_weibull, suite_banana]
    all_suites = unittest.TestSuite( suites_list )
    return all_suites

def run_tests(ttype='all'):
    all_suites = build_suite(ttype)
    # RUN
    unittest.TextTestRunner(verbosity=2).run(all_suites)

if __name__ == '__main__':
    run_tests()
