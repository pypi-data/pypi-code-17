# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.mesh import CartesianMesh
from maui.field import ScalarField
from maui.io import VTKOutput

# Create a 3d cartesian mesh
mesh_bounds = ((-50., -50.), (50., 50.))
discretization = 0.5
mesh = CartesianMesh(mesh_bounds, discretization)

# Create a vector field g from the mesh
sm = ScalarField(mesh, "g", "nounit")

# Initialize parts of the fields with some values
sm[50:60, 20:] = 3.

# Create the output
io = VTKOutput([sm], "test_io_2d")

# Write the output
io.write(cycle=5, time=0.33)
