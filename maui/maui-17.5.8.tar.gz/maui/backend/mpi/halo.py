# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'


def create_mask(indices):

    mask = []
    for i, _ in enumerate(indices[0]):

        if indices[0][i] == indices[1][i]:
            mask.append(indices[0][i])
        else:
            mask.append(slice(indices[0][i], indices[1][i]+1))

    return tuple(mask)


class TransmitHalo(object):

    def __init__(self, data, receiver, halo_location, indices):

        self.__data = data
        self.__receiver = receiver
        self.__mask = create_mask(indices)
        self.__location = halo_location

    @property
    def location(self):
        return self.__location

    @property
    def value(self):
        return self.__data[self.__mask]

    @property
    def receiver(self):
        return self.__receiver


class ReceiveHalo(object):

    def __init__(self, data, sender, halo_location, indices):

        self.__data = data
        self.__sender = sender
        self.__mask = create_mask(indices)
        self.__location = halo_location

    @property
    def value(self):
        return self.__data[self.__mask]

    @value.setter
    def value(self, value):
        self.__data[self.__mask] = value

    @property
    def sender(self):
        return self.__sender

    @property
    def location(self):
        return self.__location
