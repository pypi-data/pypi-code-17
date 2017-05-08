# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.mesh import CartesianMesh
from maui.field import ScalarField

# Create host
host_mesh_bounds = ((-50., -50., -50.), (50., 50., 50.))
host_discretization = 0.5
host_mesh = CartesianMesh(host_mesh_bounds, host_discretization)
host = ScalarField(host_mesh, "h", "nounit")

# Create Probe
target1 = ScalarField(host.partition.copy(bounds=((-40.,-20.,0.), (20.,20.,0.)), stencil=((0,0,0),(0,0,0)), shift=(0.25,0.25,0.25)), name='probe', unit='nounit')
target2 = ScalarField(host.partition.copy(bounds=((-40.,0.,-30.), (20.,0.,30.)), stencil=((0,0,0),(0,0,0)), shift=(0.25,0.25,0.25)), name='probe2', unit='nounit')
target3 = ScalarField(host.partition.copy(bounds=((0.,-50.,-30.), (0.,50.,30.)), stencil=((0,0,0),(0,0,0)), shift=(0.25,0.25,0.25)), name='probe3', unit='nounit')

host[:, :, :] = 1.
host[50:60, 20:, :] = 3.
host[:, 20:, 50:60] = 3.

host.sync()

host.cross_mesh_field_evaluation(target1)
host.cross_mesh_field_evaluation(target2)
host.cross_mesh_field_evaluation(target3)


