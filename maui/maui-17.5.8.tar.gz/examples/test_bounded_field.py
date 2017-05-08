# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.mesh import CartesianMesh
from maui.field import ScalarField


m = CartesianMesh(((-5., -5.), (1., 2.)), 0.1)

s = ScalarField(m, name="TestScalar", unit="NoUnit", bounds=((-4., -4.), (-3., 1.)))

for i in range(100):
    s.sync()
