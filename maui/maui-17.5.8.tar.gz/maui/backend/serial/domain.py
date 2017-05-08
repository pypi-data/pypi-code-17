# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'


class Domain(object):

    def __init__(self, coordinate, parent_mesh, mask=None, halos=None):
        """

        :param coordinate:
        :param parent_mesh:
        :param mask:
        :param halos:
        """

        if mask is None:
            self.mesh = parent_mesh
        else:
            self.mesh = parent_mesh[mask]

        self.coordinate = coordinate
        self.mask = mask
        self.halos = halos
