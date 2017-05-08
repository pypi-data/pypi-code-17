# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.backend import context

from maui.backend.serial.index import IndexMapper, InverseIndexMapper
from maui.backend.prototypes import Array
from numpy import zeros, ndarray


class SerialArray(Array):

    def __init__(self, domain, rank=0):

        shape = list(domain.mesh.shape)

        # Matrix column-major and (component, dim1, dim2, dim3 ... dimn) !
        for _ in range(rank):
            shape.insert(0, len(domain.mesh.shape))

        Array.__init__(self, shape, rank, domain)

        self.__data = zeros(tuple(shape), dtype=context.dtype, order='F')

        # Protect halos from being read and evaluated in the global scope!
        self.__set_index_mapper = IndexMapper(self.domain.mask)
        self.__get_index_mapper = IndexMapper(self.domain.mask, self.domain.halos)
        self.__local_to_global = InverseIndexMapper(self.domain.mask)

    def __getitem__(self, index):

        local_index = self.__get_index_mapper[index]

        if local_index is not None:
            return self.__data[local_index]
        else:
            return None

    def __setitem__(self, index, value):

        local_index = self.__set_index_mapper[index]

        if local_index is not None:

            global_index = self.__local_to_global[local_index]

            if isinstance(value, ndarray):
                # TODO: This is potentially dangerous! print local_index, global_index
                if value.shape == self.__data[local_index].shape:
                    self.__data[local_index] = value
                else:
                    self.__data[local_index] = value[global_index]
            elif isinstance(value, tuple):
                raise ValueError
            elif isinstance(value, list):
                raise ValueError
            else:
                self.__data[local_index] = value

    @property
    def d(self):
        return self.__data

