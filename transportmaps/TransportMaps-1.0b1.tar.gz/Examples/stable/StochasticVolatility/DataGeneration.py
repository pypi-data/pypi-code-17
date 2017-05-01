#!/usr/bin/env python

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

import sys, getopt
import numpy as np

import TransportMaps.Distributions.Examples.StochasticVolatility as SV

def usage():
    print('DataGeneration.py --output=<filename> [ ' + \
          '-n 945 --phi=.95 --sigma=.25 --mu=-0.5 --durbin-data]')
    print('If no value for phi, sigma or mu are provided, they are considered ' + \
          'hyperparameters')

def full_usage():
    usage()

argv = sys.argv[1:]
nsteps = 945
phi = None
sigma = None
mu = None
durbin_data = False
OUT_FNAME = None
try:
    opts, args = getopt.getopt(argv,"hn:",["output=", "phi=", "sigma=", "mu=",
                                           "durbin-data"])
except getopt.GetoptError:
    full_usage()
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        full_usage()
        sys.exit()
    elif opt == '-n':
        nsteps = int(arg)
    elif opt in ("--phi"):
        phi = float(arg)
    elif opt in ("--sigma"):
        sigma = float(arg)
    elif opt in ("--mu"):
        mu = float(arg)
    elif opt in ("--durbin-data"):
        durbin_data = True
    elif opt in ("--output"):
        OUT_FNAME = arg
if None in [OUT_FNAME]:
    full_usage()
    sys.exit(3)

#########################################
dataObs = None
if durbin_data:
    trim = nsteps
    dataObs = np.loadtxt( "data/sv.dat", skiprows = 1 )
    if nsteps > len(dataObs):
        raise ValueError("nsteps > len(dataObs)")
    if trim is not None:
        dataObs=dataObs[:trim]
    nsteps = len(dataObs)
    Xt = [None] * nsteps
else:
    dataObs, Xt = SV.generate_data(nsteps, -.5, .25, .95)
dens = SV.StocVolHyperDistribution(
    mu is None, sigma is None, phi is None,
    mu=mu, sigma=sigma, phi=phi,
    mu_sigma=1.,
    sigma_alpha=1., sigma_beta=10.,
    phi_mean=3., phi_std=1.)
for n in range(nsteps):
    dens.assimilate(y=dataObs[n], Xt=Xt[n])

dens.store(OUT_FNAME)
