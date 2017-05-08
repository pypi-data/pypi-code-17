# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import mpi4py.MPI as MPI

from maui.backend.prototypes import Context
from maui.backend import cli, argparse

def stencil(s):
    try:
        return map(int, s.split(','))
    except:
        raise argparse.ArgumentTypeError("Argument must be list of int")


class MPIContext(Context):

    def __init__(self):

        cli.add_argument('--master', type=int)
        self.__args, unknown = cli.parse_known_args()

        self.__comm = MPI.COMM_WORLD
        self.__size = self.__comm.Get_size()
        self.__rank = self.__comm.Get_rank()

        if self.__args.master is None or self.__args.master > self.__size-1:
            master_rank = 0
        else:
            master_rank = self.__args.master

        self.master_rank = master_rank

        master = False
        if self.__rank == master_rank:
            master = True

        Context.__init__(self, master=master)

    @property
    def rank(self):
        return self.__rank

    @property
    def size(self):
        return self.__size

    @property
    def comm(self):
        return self.__comm

    def setup_domain_data(self, partition, rank):
        from maui.backend.mpi.data import DataPartition
        return DataPartition(partition, rank)

    def create_partition(self, mesh, bounds=None):

        from maui.backend.mpi.partition import Partition

        dim = len(mesh.axes)
        partitions = list(MPI.Compute_dims(self.__size, dim))

        tmp = list()

        for i in range(dim):
            if partitions[i] > 1:
                tmp.append(1)
            else:
                tmp.append(0)

        stencil = (tuple(tmp), tuple(tmp))

        return Partition(mesh, tuple(partitions), tuple(stencil), bounds=bounds)

