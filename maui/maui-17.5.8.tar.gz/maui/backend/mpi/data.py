# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.backend.prototypes.helper import compute_sender, compute_receiver_halo_location
from maui.backend.mpi.array import SerialArray
from maui.backend.mpi.index import IndexBoundsHandler
from maui.backend.mpi.halo import ReceiveHalo, TransmitHalo

from maui.backend import context

import numpy as np
import mpi4py.MPI as MPI


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

        self.__d = dict()
        for key in self.__data.keys():
            self.__d[key] = self.__data[key].d

        bounds_handler_shape = list(self.partition.mesh.shape)

        for _ in range(rank):
            bounds_handler_shape.insert(0, len(self.partition.mesh.shape))

        self.__bounds_handler = IndexBoundsHandler(bounds_handler_shape)

        self.__recv_halos = dict()
        self.__send_halos = dict()

        halo_counter = 0

        for key in self.__data.keys():

            self.__recv_halos[key] = dict()
            self.__send_halos[key] = dict()
            for i in range(len(key)):
                self.__recv_halos[key][i] = []
                self.__send_halos[key][i] = []

            sender = compute_sender(key, self.__partition.domains[key].halos)

            for i in range(len(key)):
                for el in sender[i]:
                    halo_counter += 1
                    dom = self.__partition.domains[key]
                    receiver_location = compute_receiver_halo_location(dom.mesh, dom.halos, key, el)
                    self.__recv_halos[key][i].append(ReceiveHalo(self.__data[key].d, el, receiver_location, [dom.mesh.nearest_node(receiver_location[0])[0], dom.mesh.nearest_node(receiver_location[1])[0]]))

        recv_buffer = context.comm.gather([context.rank, halo_counter], root=context.master_rank)

        requests = list()

        for key in self.__data.keys():
            for k in range(len(key)):
                for halo in self.__recv_halos[key][k]:
                    requests.append(context.comm.isend([partition.rank_map[halo.sender], context.rank], dest=context.master_rank, tag=0))

        # root weiß wie viele halos jeder prozess hat
        tmp = dict()

        if context.master:
            # Send vorbereiten für data

            for j in range(context.size):
                tmp[j] = list()

            for el in recv_buffer:
                for i in range(el[1]):
                    #sender, rank
                    data = context.comm.recv(source=el[0], tag=0)
                    tmp[data[0]].append(data[1])

        MPI.Request.waitall(requests)

        mreqs = list()

        if context.master:
            for j in range(context.size):
                mreqs.append(context.comm.isend(tmp[j], dest=j, tag=1))

        MPI.Request.waitall(mreqs)
        self.__recv_halo_sources = context.comm.recv(source=context.master_rank, tag=1)
        self.__ready_for_sync = False

    def __finalize_sync_setup(self):

        requests = list()

        for key in self.__recv_halos.keys():
            for key2 in self.__recv_halos[key].keys():
                for el in self.__recv_halos[key][key2]:
                    dom = self.__partition.domains[key]
                    requests.append(context.comm.isend([key, key2, el.sender, el.location], dest=self.partition.rank_map[el.sender], tag=2))

        for key in self.partition.domains.keys():
            self.__send_halos[key] = dict()
            for i in range(len(key)):
                self.__send_halos[key][i] = list()

        for el in self.__recv_halo_sources:
            data = context.comm.recv(source=el, tag=2)
            receiver, level, sender, location = data
            dom = self.__partition.domains[sender]
            self.__send_halos[sender][level].append(TransmitHalo(self.__data[sender].d, receiver, location, [dom.mesh.nearest_node(location[0])[0], dom.mesh.nearest_node(location[1])[0]]))

        MPI.Request.waitall(requests)

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

        keys = self.partition.domains.keys()

        if keys:
            key = keys[0]
            if level is None:
                li = [i for i in range(len(key))]
            elif type(level) in (list, tuple):
                li = level
            else:
                li = [level]

            requests = list()

            for key in self.__send_halos.keys():
                for el in li:
                    for halo in self.__send_halos[key][el]:
                        requests.append(context.comm.isend(halo.value.copy(), dest=self.partition.rank_map[halo.receiver], tag=el+100))

            for key in self.__recv_halos.keys():
                for el in li:
                    for halo in self.__recv_halos[key][el]:
                        data = context.comm.recv(source=self.partition.rank_map[halo.sender], tag=el+100)
                        if isinstance(halo.value, np.ndarray):
                            halo.value[:] = data[:]
                        else:
                            halo.value = data

            MPI.Request.waitall(requests)

    @property
    def d(self):
        return self.__d

    @property
    def partition(self):
        return self.__partition

    @property
    def rank(self):
        return self.__rank
