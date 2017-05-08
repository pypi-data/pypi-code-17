# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'


from numpy import ndindex

from maui.backend.prototypes.helper import calc_local_indices, calculate_adjacency, \
    create_mask_from_indices, do_create_domain, modify_halos_and_indices
from maui.backend.serial.domain import Domain
from maui.mesh.helper import intersect_bounds

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
        self.masks_without_halos = dict()

        p = [idx for idx in ndindex(partitions)]
        for k in range(len(p)):
            self.domain_numbers[p[k]] = k

        if bounds is not None:
            self.bounds = intersect_bounds(mesh.bounds, bounds)
        else:
            self.bounds = self.mesh.bounds

        for idx in ndindex(self.partitions):
            indices = calc_local_indices(mesh.shape, self.partitions, idx)
            halos = calculate_adjacency(self.partitions, idx, stencil)
            if do_create_domain(mesh, create_mask_from_indices(indices), bounds):
                if bounds is not None:
                    halos, indices = modify_halos_and_indices(mesh, indices, halos, bounds)

                self.masks_without_halos[idx] = create_mask_from_indices(indices)
                mask = create_mask_from_indices(indices, halos)
                self.domains[idx] = Domain(idx, mesh, mask, halos)

    @property
    def meta_data(self):
        return {key: self.domains[key].mask for key in self.domains}

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
