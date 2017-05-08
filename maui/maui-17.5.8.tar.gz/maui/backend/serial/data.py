# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.backend.prototypes.helper import compute_sender, compute_receiver_halo_location
from maui.backend.serial.array import SerialArray
from maui.backend.serial.index import IndexBoundsHandler
from maui.backend.serial.halo import ReceiveHalo, TransmitHalo

import numpy


class DataPartition(object):

    def __init__(self, partition, rank=0):
        """

        :param partition:
        :param rank:
        """

        self.__partition = partition
        self.__rank = rank
        self.__data = dict()

        for key in self.partition.domains.keys():
            self.__data[key] = SerialArray(self.partition.domains[key], rank)
            #print key, self.__data[key].d.shape

        self.__d = dict()
        for key in self.__data.keys():
            self.__d[key] = self.__data[key].d

        bounds_handler_shape = list(self.partition.mesh.shape)

        for _ in range(rank):
            bounds_handler_shape.insert(0, len(self.partition.mesh.shape))

        self.__bounds_handler = IndexBoundsHandler(bounds_handler_shape)

        self.__recv_halos = dict()
        self.__send_halos = dict()

        for key in self.__data.keys():

            self.__recv_halos[key] = dict()
            self.__send_halos[key] = dict()
            for i in range(len(key)):
                self.__recv_halos[key][i] = []
                self.__send_halos[key][i] = []

            sender = compute_sender(key, self.__partition.domains[key].halos)

            for i in range(len(key)):
                for el in sender[i]:
                    dom = self.__partition.domains[key]
                    receiver_location = compute_receiver_halo_location(dom.mesh, dom.halos, key, el)
                    self.__recv_halos[key][i].append(ReceiveHalo(self.__data[key].d, el, receiver_location, [dom.mesh.nearest_node(receiver_location[0])[0], dom.mesh.nearest_node(receiver_location[1])[0]]))

        self.__ready_for_sync = False

    def __finalize_sync_setup(self):
        for key in self.__recv_halos.keys():
            for key2 in self.__recv_halos[key].keys():
                for el in self.__recv_halos[key][key2]:
                    dom = self.__partition.domains[el.sender]
                    self.__send_halos[el.sender][key2].append(TransmitHalo(self.__data[el.sender].d, key, el.location, [dom.mesh.nearest_node(el.location[0])[0], dom.mesh.nearest_node(el.location[1])[0]]))

    def __getitem__(self, item):

        value = dict()
        for key in self.__data.keys():
            tmp = self.__data[key][self.__bounds_handler[item]]
            if tmp is not None:
                value[key] = tmp

        if len(value) >= 1:
            return value

        return None

    def __setitem__(self, item, value):
        for key in self.__data.keys():
            self.__data[key][self.__bounds_handler[item]] = value

    def sync(self, level=None):
        if not self.__ready_for_sync:
            self.__finalize_sync_setup()
            self.__ready_for_sync = True

        for key in self.__recv_halos.keys():

            if level is None:
                li = [i for i in range(len(key))]
            elif type(level) in (list, tuple):
                li = level
            else:
                li = [level]

            for el in li:
                for halo in self.__recv_halos[key][el]:
                    for send_halo in self.__send_halos[halo.sender][el]:
                        if send_halo.receiver == key:
                            if isinstance(halo.value, numpy.ndarray):
                                halo.value[:] = send_halo.value[:]
                            else:
                                halo.value = send_halo.value

    @property
    def d(self):
        return self.__d

    @property
    def partition(self):
        return self.__partition

    @property
    def rank(self):
        return self.__rank
