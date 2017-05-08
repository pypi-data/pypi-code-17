# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'marco.muetze <at> tu-dresden.de'


from .helper import check_bounds_and_get_dimension
from .prototypes import Mesh
import numpy as np
from scipy.interpolate import RegularGridInterpolator


def calculate_bounds(axes):

    lower = []
    upper = []
    num_of_axes = len(axes)

    for idx in range(num_of_axes):
        if axes[idx][0] < axes[idx][-1]:
            lower.append(axes[idx][0])
            upper.append(axes[idx][-1])
        else:
            upper.append(axes[idx][0])
            lower.append(axes[idx][-1])

    return tuple(lower), tuple(upper)


def calculate_shape(axes):

    shape = []

    if type(axes) in (tuple, list):
        for dim in range(len(axes)):
            if type(axes[dim]) is np.ndarray:
                shape.append(len(axes[dim]))
            else:
                raise TypeError
    elif type(axes) is np.ndarray:
        shape.append(len(axes))
    else:
        raise TypeError

    return tuple(shape)


def calculate_center(bounds):

    dimension = check_bounds_and_get_dimension(bounds)
    center_position = []

    for i in range(dimension):
        center_position.append((bounds[1][i] + bounds[0][i]) * 0.5)

    return tuple(center_position)


class RectilinearMesh(Mesh):

    interpolator = RegularGridInterpolator

    def __init__(self, axes, axes_names=('x', 'y', 'z'), unit='m'):
        """ RectilinearMesh

            :param axes: Values of axis nodes as tuple of 1D np.arrays.
            :param axes_names: Coordinate system axes names.
            :param unit: Unit of mesh values.

        """

        bounds = calculate_bounds(axes)
        center = calculate_center(bounds)
        shape = calculate_shape(axes)

        self.__axes = axes
        self.__shape = shape

        Mesh.__init__(self, bounds, axes_names=axes_names, unit=unit)

        self.__center_index = self.nearest_node(center)[0]

    def __getitem__(self, item):
        # item umpopeln damit tuple of slice passt!
        new_axes = []

        # This only works when len(item) equals the dimension of the mesh and will not work for None!
        for i, x in enumerate(item):
            new_axes.append(self.axes[i][x])

        return RectilinearMesh(tuple(new_axes), self.axes_names, self.unit)

    def copy(self):
        new_axes = []

        for axe in self.axes:
            new_axes.append(axe.copy())

        return RectilinearMesh(tuple(new_axes), self.axes_names, self.unit)

    def shift(self, offset):

        # Update bounds!
        low = np.array(self.bounds[0])
        high = np.array(self.bounds[1])
        tmp = np.array(offset)

        self._bounds = (tuple(low+tmp), tuple(high+tmp))

        assert len(offset) == len(self.axes)

        new_axes = []

        for axe in self.axes:
            new_axes.append(axe.copy())

        for i, d in enumerate(offset):
            new_axes[i] += d

        self.__axes = tuple(new_axes)
        return self

    @property
    def pitch(self):

        dimension = self._dimension  # len(self._axes)
        pitch = [0.] * dimension

        for dim in range(dimension):
            axis_len = len(self.__axes[dim])
            # create empty numpy array
            coordinates = np.zeros(axis_len-1)
            for idx in range(axis_len-1):
                coordinates[idx] = (self.__axes[dim][idx+1]-self.__axes[dim][idx])

            pitch[dim] = coordinates.copy()

        return tuple(pitch)

    @property
    def axes(self):
        return self.__axes

    @property
    def shape(self):
        return self.__shape

    @property
    def center_index(self):
        return self.__center_index

    @property
    def minimum_pitch(self):
        """ Returns the minimal pitch between two neighboring nodes of the mesh in each direction.

        :return: Minimal pitch in each direction.
        """
        pitch = self.pitch
        minimal_pitch = []

        for p in pitch:
            minimal_pitch.append(min(p))

        return min(minimal_pitch)

    def nearest_node(self, position):

        idx = []
        point = []
        for i in range(len(self.axes)):
            if position[i] < self.bounds[0][i] or position[i] > self.bounds[1][i]:
                raise ValueError('The given position is outside the mesh bounds!')

            tmp = (np.abs(self.axes[i]-position[i])).argmin()
            idx.append(int(tmp))
            point.append(self.axes[i][tmp])

        return tuple(idx), tuple(point), np.linalg.norm(np.asarray(position)-np.asarray(point))

    def surrounding_nodes(self, position):
        """ Returns nearest node indices and direction of opposite node.

        :param position: Position inside the mesh to search nearest node for as (x,y,z)
        :return: Nearest node indices and direction of opposite node.
        """

        n_node_index, n_node_position, n_node_error = self.nearest_node(position)

        if n_node_error == 0.0:

            index_mod = []

            for i in range(len(n_node_index)):

                new_point = np.asarray(n_node_position)
                new_point[i] += 1.e-5*np.abs(new_point[i])

                try:
                    self.nearest_node(tuple(new_point))
                    index_mod.append(-1)
                except ValueError:
                    index_mod.append(1)

        else:
            # Check if node_position is larger or smaller in resp. axes than position

            index_mod = []

            for i in range(len(n_node_index)):
                if n_node_position[i] > position[i]:
                    index_mod.append(-1)
                else:
                    index_mod.append(1)

        return tuple(n_node_index), tuple(index_mod)
