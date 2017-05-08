# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'christoph.statz <at> tu-dresden.de'

from .helper import check_bounds_and_get_dimension
from .rectilinear import RectilinearMesh

import numpy as np


def calculate_axes(bounds, pitch):

    dimension = check_bounds_and_get_dimension(bounds)

    axes = []

    tmp_bounds = [list(x) for x in bounds]

    for i in range(dimension):
        tmp_bounds[1][i] += pitch[i]
        axes.append(np.arange(tmp_bounds[0][i], tmp_bounds[1][i], pitch[i]))

    return tuple(axes)


class RectangularMesh(RectilinearMesh):

    def __init__(self, bounds, pitches, axes_names=('x', 'y', 'z'), unit='m'):
        """ RectangularMesh

        :param bounds: Lower and upper bounds of mesh ((x_low, y_low, z_low), (x_high, y_high, z_high)).
        :param pitches: Maximum pitches between neighboring nodes in each direction.
        :param axes_names: Names of the coordinate system axes.
        :param unit: Unit of bounds, pitch and mesh related quantities.

        """

        if not isinstance(pitches, tuple):
            raise TypeError('Pitch needs to be instance of tuple.')

        axes = calculate_axes(bounds, pitches)
        RectilinearMesh.__init__(self, axes, axes_names=axes_names, unit=unit)
