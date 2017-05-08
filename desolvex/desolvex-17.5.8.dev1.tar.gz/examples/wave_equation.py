# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from desolvex.domain import CartesianDomain
from desolvex.solver import ExplicitSolver
from desolvex.helper import ObjectSwapper
from desolvex.stopcriteria import IterationStopCriterion
from desolvex.source import PointSource
from desolvex.source.functions import ricker
from maui.io import VTKOutput


# Define the coordinate names for the fields
coordinates = ['x', 'y', 'z']

# Define the differential operator and update function
def laplace_3d(d, n):
    d[1:-1, 1:-1, 1:-1] = 1./2. * (n[:-2, 1:-1, 1:-1] + n[2:, 1:-1, 1:-1] +
                          n[1:-1, :-2, 1:-1] + n[1:-1, 2:, 1:-1] +
                          n[1:-1, 1:-1, :-2] + n[1:-1, 1:-1, 2:] - 6.*n[1:-1, 1:-1, 1:-1])

def time_integration_step(p, n, m, d, c):
    p[:, :, :] = 2.*n[:, :, :] - m[:, :, :] + 0.32*(c[:,:,:])**2*d[:, :, :]


# Define the fields and variables
wave_equation_fields = {'node': {'c': 'm/s', 'e': 'V/m', 'e+': 'V/m', 'e-': 'V/m', 'd': 'V/m**2'}}
wave_equation_variables = {'t': 0., 'dt': 0.57 * 0.005/299792458., 'ds': 0.005}

# Allocate the computational domain and set the field values
c = CartesianDomain(((-0.5,-0.6,-0.7), (0.5,0.6,0.7)), wave_equation_variables['ds'], wave_equation_fields, wave_equation_variables)
c.fields['c'][:,:,:] = 1.

# Define domain related updates
def time_update(variables):
    variables['t'] = variables['dt']*variables['iteration']

# Define which fields are written as simulation output
io = VTKOutput([c.fields['e'], c.fields['c']], 'wave')

def generate_output(io, stop_criterion):
    if stop_criterion.int_value % 10 == 0:
        io.write(cycle=stop_criterion.int_value)

# Define a source function
f0 = 3e9
t0 = 50.*c.variables['dt']
a = 1.
s = PointSource((0.01, 0.05, 0.05), c.fields['e'], ricker, parameter=[a, f0, t0])

# Define a stop criterion for the fields
stop_criterion = IterationStopCriterion(c.variables, maximum_iterations=800)

# Define actions neccessary to solve the pde
state_fields = ObjectSwapper([c.fields['e+'], c.fields['e'], c.fields['e-']])

actions = list()

actions.append([time_update, c.variables])
actions.append([laplace_3d, c.fields['d'], [state_fields, 1]])
actions.append([s.set, [c.variables, 't']])
actions.append([time_integration_step, state_fields, c.fields['d'], c.fields['c']])
actions.append([generate_output, io, stop_criterion])
actions.append([state_fields.swap])

# Instantiate the explicit solver
s = ExplicitSolver(actions, stop_criterion)

# Run the simulation
s.solve()

