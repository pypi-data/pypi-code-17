# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.backend.prototypes import Context
from maui.backend import cli, argparse


def stencil(s):
    try:
        return map(int, s.split(','))
    except:
        raise argparse.ArgumentTypeError("Argument must be list of int")


class SerialContext(Context):

    def __init__(self):

        cli.add_argument('--partition', type=stencil)
        self.__args, unknown = cli.parse_known_args()

        Context.__init__(self, master=True)

    def setup_domain_data(self, partition, rank):
        from maui.backend.serial.data import DataPartition
        return DataPartition(partition, rank)


    def create_partition(self, mesh, bounds=None):

        from maui.backend.serial.partition import Partition

        partitions = []

        dim = len(mesh.axes)

        tmp = list() 

        if self.__args.partition is None:

            for _ in range(dim):
                partitions.append(1)
                tmp.append(0)

        else:
            if len(self.__args.partition) == dim:
                partitions = self.__args.partition
            elif len(self.__args.partition) < dim:
                for _ in range(dim-len(self.__args.partition)):
                    partitions.append(1)
            else:
                partitions = self.partitions[:dim]

            for i in range(dim):
                if partitions[i] > 1:
                    tmp.append(1)
                else:
                    tmp.append(0)

        stencil = (tuple(tmp), tuple(tmp))

        return Partition(mesh, tuple(partitions), tuple(stencil), bounds=bounds)
