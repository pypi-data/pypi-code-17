# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from .field import Field


class ScalarField(Field):

    def __init__(self, mesh, name, unit, bounds=None):
        """ Scalar field class.

        :param partition: Partition or Mesh, coordinate space associated with the field.
        :param name: String, unique name of the field/variable.
        :param unit: String, physical unit associated with the field.
        :param interpolation: Interpolator, class to obtain value from the field by coordinate.
        :param bounds: 2-Tuple of Tuples, bounds of the field inside the mesh.

        """

        Field.__init__(self, mesh, name, unit, rank=0, bounds=bounds)

