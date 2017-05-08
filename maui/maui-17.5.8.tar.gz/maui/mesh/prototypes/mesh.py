# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.mesh.helper import check_bounds_and_get_dimension

class Mesh(object):

    def __init__(self, bounds, axes_names=('x', 'y', 'z'), unit='m'):
        """ Constructor of Mesh

        :param bounds: mesh boundary ((x1,y1,z1),(x2,y2,z2))
        :param axes_names: type of coordinate system
        :param unit: unit of mesh values
        """
        self._bounds = bounds
        self._axes_names = axes_names
        self._unit = unit

        # calculate implicit values
        self._dimension = check_bounds_and_get_dimension(self._bounds)

    @property
    def bounds(self):
        return self._bounds

    @property
    def axes_names(self):
        return self._axes_names

    @property
    def unit(self):
        return self._unit

    @property
    def dimension(self):
        return self._dimension

    def min_bound(self):
        """ get bound minimum of mesh """
        return min(self._bounds)

    def max_bound(self):
        """ get bound maximum of mesh"""
        return max(self._bounds)
