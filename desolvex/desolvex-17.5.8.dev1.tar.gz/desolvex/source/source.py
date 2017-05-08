# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np


class Source(object):

    def __init__(self, field, source_function, parameter, softsource=False):

        self._field = field
        self._source_function = source_function
        self._parameter = parameter
        self._softsource = softsource

    @property
    def softsource(self):
        return self._softsource
        
    @property
    def field(self):
        return self._field

    @property
    def source_function(self):
        return self._source_function

    @property
    def parameter(self):
        return self._parameter


class PointSource(Source):

    def __init__(self, point, field, source_function, parameter=None):

        Source.__init__(self, field, source_function, parameter)

        self.position = point
        self._point = point
        self._index, _, _ = self.field.partition.mesh.nearest_node(point)

    def value(self, t):
        return self._source_function(float(t), self._parameter)

    @property
    def point_coord(self):
        return self._point

    def set(self, t):
        if self.field[self._index] is not None:
            for key in self.field[self._index].keys():
                if self.softsource:
                    self.field[self._index] = self.field[self._index][key] + self.value(float(t))
                else:
                    self.field[self._index] = self.value(float(t))


class DataPointSource(PointSource):

    def __init__(self, point, field, data, dt, reverse_time=True):

        if reverse_time:
            data.reverse()

        self.data = data

        self.dt = dt
        point = np.asarray(point)

        PointSource.__init__(self, point, field, [], [])

        self.position = point
        self._point = point
        self._index, _, _ = self.field.partition.mesh.nearest_node(point)

    def value(self, t):
        return self.data[int(t//self.dt)]


class PlaneSource(Source):

    def __init__(self, bounds, field, source_function, parameter=None):

        Source.__init__(self, field, source_function, parameter)

        self.__bounds = bounds
        self.__start_index, _, _ = self.field.partition.mesh.nearest_node(bounds[0])
        self.__stop_index, _, _ = self.field.partition.mesh.nearest_node(bounds[1])

        idx = []
        for i in range(len(self.__start_index)):
            idx.append(slice(self.__start_index[i], self.__stop_index[i]+1))

        self.__index = tuple(idx)

    @property
    def index(self):
        return self.__index

    def value(self, t):
        return self._source_function(float(t), self._parameter)

    def set(self, t):
        if self.field[self.__index] is not None:
            for key in self.field[self.__index].keys():
                if self.softsource:
                    self.field[self.__index] = self.field[self.__index][key] + self.value(float(t))
                else:
                    self.field[self.__index] = self.value(float(t))


class DataPlaneSource(PlaneSource):

    def __init__(self, bounds, field, data, dt, reverse_time=True):

        if reverse_time:
            data.reverse()

        self.data = data
        self.dt = dt

        PlaneSource.__init__(self, bounds, field, [], [])

    def value(self, t):
        return self.data[int(np.floor(t/self.dt))]

    def set(self, t):
        if self.field[self.index] is not None:
            for key in self.field[self.index].keys():
                if self.softsource:
                    self.field[self.index] = self.field[self.index][key] + self.value(float(t))[key]
                else:
                    self.field[self.index] = self.value(float(t))[key]
