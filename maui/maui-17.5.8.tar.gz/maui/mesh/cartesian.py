# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from .rectangular import *


class CartesianMesh(RectangularMesh):

    def __init__(self, bounds, pitch, axes_names=('x', 'y', 'z'), unit='m'):
        """ CartesianMesh

        :param bounds: Lower and upper bounds of mesh ((x_low, y_low, z_low), (x_high, y_high, z_high)).
        :param pitch: Maximum pitch between neighboring nodes same for all directions.
        :param axes_names: Names of the coordinate system axes.
        :param unit: Unit of bounds, pitch and mesh related quantities.

        """

        pitches = tuple([pitch for i in range(len(bounds[0]))])
        RectangularMesh.__init__(self, bounds, pitches, axes_names=axes_names, unit=unit)
