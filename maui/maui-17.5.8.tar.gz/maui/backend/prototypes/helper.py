# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np


def compute_receiver_halo_location(mesh, halos, idx, sender):

    halo_direction = np.asarray(idx)-np.asarray(sender)
    high_sender = any(h < 0 for h in halo_direction)

    fr = []
    to = []

    for i, el in enumerate(halo_direction):
        if el == 0:
            fr.append(mesh.axes[i][0])
            to.append(mesh.axes[i][-1])
        else:
            if high_sender:
                fr.append(mesh.axes[i][-1*halos[1][i]])
                to.append(mesh.axes[i][-1])
            else:
                fr.append(mesh.axes[i][0])
                to.append(mesh.axes[i][halos[0][i]-1])

    return fr, to


def compute_sender(idx, halos):

    def iterate_sender(position, direction, sender, level=0):

        for i, el in enumerate(direction):
            new_position = list(position)
            new_position[i] = position[i] + el

            if new_position[i] != position[i] and new_position[i] >= 0:
                sender[level].append(tuple(new_position))
                new_direction = list(direction)
                new_direction[i] = 0
                iterate_sender(tuple(new_position), tuple(new_direction), sender, level=level+1)

    sender = {}
    for i in range(len(idx)):
        sender[i] = []

    halo = tuple(-1*(np.array(halos[0]) > 0).astype('int'))
    iterate_sender(idx, halo, sender)
    halo = tuple((np.array(halos[1]) > 0).astype('int'))
    iterate_sender(idx, halo, sender)

    for el in sender.keys():
        sender[el] = list(set(sender[el]))

    return sender


def create_mask_from_indices(indices, halos=None):

    if halos is None:
        tmp = []
        for k in range(len(indices[0])):
            tmp.append(0)
        halos = (tuple(tmp), tuple(tmp))

    mask = []
    for i, _ in enumerate(indices[0]):

        mod = 0

        if indices[0][i] == indices[1][i]:
            mod = 1

        mask.append(slice(indices[0][i]-halos[0][i], indices[1][i]+halos[1][i]+mod))

    return tuple(mask)


def calc_local_indices(shape, num_partitions, coordinate):
    """ calculate local indices, return start and stop index per dimension per process for local data field

    :param shape: global shape of data
    :param num_partitions: number of partition for each dimension (from MPI.Compute_dims())
    :param coordinate: cartesian coordinate descriptor (from CARTESIAN_COMMUNICATOR.Get_coords(rank))

    :return: tuple of start/stop index per dimension ((start_x, stop_x), (start_y, stop_y), ...)
    """
    dimension = len(shape)
    # check matching of cartesian communicator and shape
    assert dimension == len(num_partitions)

    decomposed_shapes = []
    # build shape list for every dimension
    for idx in range(dimension):
        local_shape = shape[idx] // num_partitions[idx]
        temp_shape_list = []

        for _ in range(num_partitions[idx]):
            temp_shape_list.append(local_shape)

        # expand local partitions to match global shape
        for j in range(shape[idx] % num_partitions[idx]):
            temp_shape_list[j] += 1

        # decomposed_shapes[dimension][partition]
        decomposed_shapes.append(temp_shape_list)

    # calculate indices for partitions
    indices = []

    # TODO: redefine calculation -> first select and calculate
    for i in range(dimension):

        temp_index_list = []

        start_idx = 0
        end_idx = 0

        for j in range(num_partitions[i]):

            end_idx = end_idx + decomposed_shapes[i][j]
            temp_index_list.append([start_idx, end_idx])
            start_idx = end_idx

        indices.append(temp_index_list)

    start_index = []
    stop_index = []
    shape = []

    # select partition, start and stop index
    for idx in range(dimension):
        start_index.append(indices[idx][coordinate[idx]][0])
        stop_index.append(indices[idx][coordinate[idx]][1])
        shape.append(decomposed_shapes[idx][coordinate[idx]])

    shape = tuple(shape)
    start_index = tuple(start_index)
    stop_index = tuple(stop_index)
    return start_index, stop_index, shape


def calculate_adjacency(partitions, coordinate, stencil):

    if len(partitions) is not len(coordinate):
        raise ValueError

    for i, coord in enumerate(coordinate):
        if coord > partitions[i]-1:
            raise ValueError("Coordinate %i in dimension %i should not exist!" % (coord, i))

    low = []
    high = []

    for i, p in enumerate(coordinate):

        if p is 0:
            low.append(0)
        else:
            low.append(stencil[0][i])

        if p is partitions[i]-1:
            high.append(0)
        else:
            high.append(stencil[1][i])

    return tuple(low), tuple(high)


def do_create_domain(mesh, mask, bounds):

    if bounds is None:
        return True

    for i, b in enumerate(mesh.bounds[0]):
        if b > bounds[1][i]:
            raise ValueError('Higher bounds out of global mesh bounds.')

    for i, b in enumerate(mesh.bounds[1]):
        if b < bounds[0][i]:
            raise ValueError('Lower bounds out of global mesh bounds.')

    if mask is not None:
        try:
            do_create_domain(mesh[mask], mask=None, bounds=bounds)
        except ValueError:
            return False

    return True


def modify_halos_and_indices(mesh, indices, halos, bounds):

    halos_ = list(list(x) for x in halos)
    indices_ = list(list(x) for x in indices)

    test_bounds = mesh[create_mask_from_indices(indices)].bounds

    for i, b in enumerate(bounds[0]):

        lb = list(test_bounds[0])
        hb = list(test_bounds[1])

        if b >= test_bounds[0][i]:
            halos_[0][i] = 0 # no lower neighbor!
            lb[i] = bounds[0][i]
            indices_[0][i] = mesh.nearest_node(lb)[0][i]
        if bounds[1][i] <= test_bounds[1][i]:
            halos_[1][i] = 0 # no higher neighbor!
            hb[i] = bounds[1][i]
            indices_[1][i] = mesh.nearest_node(hb)[0][i] + 1

    halos = tuple(tuple(x) for x in halos_)
    indices = tuple(tuple(x) for x in indices_)

    return halos, indices

