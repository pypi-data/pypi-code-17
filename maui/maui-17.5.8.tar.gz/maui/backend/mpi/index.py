# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np


class InverseIndexMapper(object):
    """ class to map local indexes to global ones """
    def __init__(self, mask, halos=None):
        """ Constructor of class InverseIndexMapper

        :param start_index: local start index as tuple (x1,y1,z1) or slice
        :param stop_index: local stop index as tuple (x2,y2,z3) or slice
        """

        if halos is None:
            tmp = tuple([0 for _ in range(len(mask))])
            halos = (tmp, tmp)

        self.__mask = mask

    def __getitem__(self, index):

        return self.local_to_global(index)

    def slice_local_to_global(self, index_slice, axis=0):
        """ Calculate start and stop index for mapping sliced index

        :param index_slice: sliced index?
        :param axis: current axis to calculate
        :return: slice object as calculated
        """

        local_start = self.int_local_to_global_start(index_slice.start, axis)
        local_stop = self.int_local_to_global_stop(index_slice.stop, axis)

        return slice(local_start,local_stop,index_slice.step)


    def local_to_global(self, index):
        """ Calculate local index from global index
        :param index: input index
        :return: local index for data
        """

        if (type(index) is int) or (type(index) is slice):
            if len(self.__mask) > 1:
                raise IndexError('check length of parameter index')
            # 1D array
            if type(index) is int:
                return self.int_local_to_global(index)

            elif type(index) is slice:
                return self.slice_local_to_global(index)

            else:
                raise IndexError('check data type of index to be integer or slice')

        elif type(index) is tuple:

            local_index = []

            for k, item in enumerate(index):
                if k < len(self.__mask):

                    if type(item) is slice:
                        temp_index = self.slice_local_to_global(item, k)

                    elif type(item) in [int, np.int64, np.int32]:
                        temp_index = self.int_local_to_global(item, k)

                    if temp_index is None:
                        return temp_index

                else:
                    temp_index = item

                local_index.append(temp_index)

            return tuple(local_index)
        else:
            raise IndexError('check index for correct length and type')

    def int_local_to_global_start(self, index, axis=0):
        """ Calculate local index from global index from start_index

        :param index: global index as integer
        :param axis: current axis to process
        :return:
        """

        return index + self.__mask[axis].start

    def int_local_to_global_stop(self, index, axis=0):
        """ Calculate local index from global index from stop_index

        :param index: global index as integer
        :param axis: current axis to process
        :return:
        """

        return index + self.__mask[axis].start

    def int_local_to_global(self, index, axis=0):
        """ Calculate local index from global index for integer input

        :param index: global index as integer
        :param axis: current axis to process
        :return:
        """

        return index + self.__mask[axis].start


class IndexMapper(object):
    """ class to map global indexes to local ones """
    def __init__(self, mask, halos=None):
        """ Constructor of class IndexMapper

        :param start_index: local start index as tuple (x1,y1,z1) or slice
        :param stop_index: local stop index as tuple (x2,y2,z3) or slice
        """

        if halos is None:
            tmp = tuple([0 for _ in range(len(mask))])
            halos = (tmp, tmp)

        self.__halos = halos
        self.__mask = mask

    def __getitem__(self, index):
        return self.global_to_local(index)

    def slice_global_to_local(self, index_slice, axis=0):
        """ Calculate start and stop index for mapping sliced index

        :param index_slice: sliced index?
        :param axis: current axis to calculate
        :return: slice object as calculated
        """
        if index_slice.stop < self.__mask[axis].start+self.__halos[0][axis]:
            return None

        if index_slice.start > self.__mask[axis].stop-self.__halos[1][axis]:
            return None

        local_start = self.int_global_to_local_start(index_slice.start, axis)
        local_stop = self.int_global_to_local_stop(index_slice.stop, axis)

        return slice(local_start,local_stop,index_slice.step)


    def global_to_local(self, index):
        """ Calculate local index from global index

        :param index: input index
        :return: local index for data
        """
        if (type(index) is int) or (type(index) is slice):
            if len(self.__mask) > 1:
                raise IndexError('check length of parameter index')
            # 1D array
            if type(index) is int:
                return self.int_global_to_local(index)

            elif type(index) is slice:
                return self.slice_global_to_local(index)

            else:
                raise IndexError('check data type of index to be integer or slice')

        elif type(index) is tuple:
            #if len(index) is not len(self.__mask):
            #    raise IndexError('check length of parameter index')

            local_index = []

            for k, item in enumerate(index):
                if k < len(self.__mask):

                    if type(item) is slice:
                        temp_index = self.slice_global_to_local(item, k)

                    elif type(item) in [int, np.int64, np.int32]:
                        temp_index = self.int_global_to_local(item, k)

                    if temp_index is None:
                        return temp_index

                else:
                    temp_index = item

                local_index.append(temp_index)

            return tuple(local_index)
        else:
            raise IndexError('check index for correct length and type')

    def int_global_to_local_start(self, index, axis=0):
        """ Calculate local index from global index from start_index

        :param index: global index as integer
        :param axis: current axis to process
        :return:
        """
        if index >= self.__mask[axis].stop-self.__halos[1][axis]:
            return None

        if index < self.__mask[axis].start:
            return 0

        return index-self.__mask[axis].start

    def int_global_to_local_stop(self, index, axis=0):
        """ Calculate local index from global index from stop_index

        :param index: global index as integer
        :param axis: current axis to process
        :return:
        """
        if index < self.__mask[axis].start+self.__halos[0][axis]:
            return None

        if index > self.__mask[axis].stop:
            return self.__mask[axis].stop-self.__mask[axis].start

        return index-self.__mask[axis].start

    def int_global_to_local(self, index, axis=0):
        """ Calculate local index from global index for integer input

        :param index: global index as integer
        :param axis: current axis to process
        :return:
        """

        # Warum >= an dieser Stelle. Eigentlich sollte > ausreichend sein! Test!
        if index >= self.__mask[axis].stop-self.__halos[1][axis]:
            return None

        if index < self.__mask[axis].start+self.__halos[0][axis]:
            return None

        return index-self.__mask[axis].start


class IndexBoundsHandler(object):
    """ class to handle bound errors in mpi wrapper """
    def __init__(self, global_shape):
        """ Constructor of IndexBoundsHandler

        :param global_shape: global shape of data where to check bounds
        """
        self._global_shape = global_shape

    def __getitem__(self, index):
        return self.out_of_bounds(index)

    def int_out_of_bounds(self, index, axis=0):
        """ examples if index is out of local processing bounds

        function is used to perform examples for index of type integer
        :param index: global index to examples as type int
        :param axis: current axis to examples
        :return: return input or raise error
        """
        #if index >= self._global_shape[axis]:
        if index > self._global_shape[axis]:
            raise IndexError('index is larger than the upper bound')

        # wrap around index if negative like in python
        if index < 0:
            index += self._global_shape[axis]
            #warnings.warn('warp around may occur')

        # check for invalid wrap around
        if index < 0:
            raise IndexError('index is smaller than the lower bound')

        return index

    def slice_out_of_bounds(self, index, axis=0):
        start = index.start
        stop = index.stop

        if start is None:
            start = 0

        if stop is None:
            stop = self._global_shape[axis]

        # stop-=1

        index_start = self.int_out_of_bounds(start, axis)
        index_stop = self.int_out_of_bounds(stop, axis)

        return slice(index_start, index_stop, index.step)

    def out_of_bounds(self, index):
        """ Check index for out of bounds

        :param index: index as integer, tuple or slice
        :return: local index as tuple
        """
        if type(index) is int:
            return self.int_out_of_bounds(index)

        elif type(index) is slice:
            return self.slice_out_of_bounds(index)

        elif type(index) is tuple:

            local_index = []

            for k, item in enumerate(index):

                if type(item) is slice:
                    temp_index = self.slice_out_of_bounds(item, k)

                elif type(item) is int:
                    temp_index = self.int_out_of_bounds(item, k)
                # FIXME: will fail if item is no int or slice!
                if temp_index is None:
                    return temp_index

                local_index.append(temp_index)

            return tuple(local_index)
