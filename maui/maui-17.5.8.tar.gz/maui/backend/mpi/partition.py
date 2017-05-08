# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from numpy import ndindex
from maui.backend.prototypes.helper import calc_local_indices, calculate_adjacency, \
    create_mask_from_indices, do_create_domain, modify_halos_and_indices
from maui.backend.mpi.domain import Domain
from maui.mesh.helper import intersect_bounds
from maui.backend import context

import mpi4py.MPI as MPI
import numpy as np

# TODO: Partition prototype is needed


class Partition(object):

    def __init__(self, mesh, partitions, stencil, bounds=None):
        """ Mesh partitioning.

        :param mesh: Mesh, the mesh instance that is to be partitioned.
        :param partitions: Tuple, number of partitions in each dimension of the mesh.
        :param stencil: 2-Tuple of Tuple, stencil/footprint of the communication/halos for a multi-domain Field.
        :param bounds: 2-Tuple of Tuple, bounds of the partition inside the mesh.
        """

        # todo: implement properties as properties
        self.mesh = mesh
        self.partitions = partitions
        self.stencil = stencil

        # TODO: @property protect
        self.domains = dict()
        self.domain_numbers = dict()
        # TODO: populate using create_mask_from_indices, distribute using collective communication
        self.masks_without_halos = dict()

        if bounds is not None:
            self.bounds = intersect_bounds(mesh.bounds, bounds)
        else:
            self.bounds = self.mesh.bounds

        p = [idx for idx in ndindex(self.partitions)]

        for k in range(len(p)):
            self.domain_numbers[p[k]] = k

        # TODO: Hier sind schon wichtige informationen für die Kommunikation!!!
        idx = p[context.rank]

        self.__rank_map = dict()

        for i, el in enumerate(p):
            self.__rank_map[el] = i

        indices = calc_local_indices(mesh.shape, self.partitions, idx)
        halos = calculate_adjacency(self.partitions, idx, stencil)

        if do_create_domain(mesh, create_mask_from_indices(indices), bounds):
            if bounds is not None:
                halos, indices = modify_halos_and_indices(mesh, indices, halos, bounds)

            mask = create_mask_from_indices(indices, halos)
            self.domains[idx] = Domain(idx, mesh, mask, halos)

        dim = len(self.bounds[0])

        tmp = list()

        if self.domains.keys():
            for i in range(dim):
                tmp.append([self.domains[idx].mask[i].start, self.domains[idx].mask[i].stop])

        data = context.comm.allgather({idx: tmp})

        self.__meta_data = dict()

        for i in range(context.size):
            key = data[i].keys()[0]
            if data[i][key]:
                mask = []
                for j in range(dim):
                    mask.append(slice(data[i][key][j][0], data[i][key][j][1]))

                self.__meta_data[key] = tuple(mask)

    @property
    def meta_data(self):
        return self.__meta_data

    def copy(self, bounds=None, stencil=None, shift=None):

        if stencil is None:
            stencil = self.stencil

        if bounds is None:
            bounds = self.bounds
        else:
            bounds = intersect_bounds(self.bounds, bounds)

        mesh = self.mesh.copy()

        if shift is not None:
            mesh.shift(shift)

        return Partition(mesh, self.partitions, stencil, bounds)

    @property
    def rank_map(self):
        return self.__rank_map
