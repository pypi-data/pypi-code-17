# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np


class PointProbe(object):

    def __init__(self, position, field, parameter=None):

        self.field = field
        self.position = position

        self.index, _, _ = self.field.partition.mesh.nearest_node(position)
        self.data = []

    @property
    def value(self):
        if self.field[self.index] is not None:
            return self.field[self.index].values()
        else:
            return 0.

    def get(self):
        self.data.append(self.value)


class PlaneProbe(object):

    def __init__(self, bounds, field, time_interval=None):

        self.__field = field
        self.__bounds = bounds
        self.__start_index, _, _ = self.__field.partition.mesh.nearest_node(bounds[0])
        self.__stop_index, _, _ = self.__field.partition.mesh.nearest_node(bounds[1])

        idx = []
        for i in range(len(self.__start_index)):
            idx.append(slice(self.__start_index[i], self.__stop_index[i]+1))

        self.__index = tuple(idx)

        self.data = []

    @property
    def index(self):
        return self.__index

    @property
    def bounds(self):
        return self.__bounds

    @property
    def field(self):
        return self.__field

    @property
    def value(self):
        tmp = self.__field[self.__index]
        ret = dict()
        for key in tmp.keys():
            ret[key] = tmp[key].copy()
        return ret

    def get(self):
        self.data.append(self.value)
