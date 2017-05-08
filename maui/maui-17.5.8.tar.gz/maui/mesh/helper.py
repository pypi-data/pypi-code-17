# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'christoph.statz <at> tu-dresden.de'


def intersect_bounds(bds_a, bds_b):

    assert len(bds_a[0]) == len(bds_b[0])

    new_bounds = []
    tmp = []

    for i, bd in enumerate(bds_a[0]):
        if bds_a[0][i] >= bds_b[0][i]:
            tmp.append(bds_a[0][i])
        else:
            tmp.append(bds_b[0][i])

    new_bounds.append(tuple(tmp))
    tmp = []

    for i, bd in enumerate(bds_a[1]):
        if bds_a[1][i] <= bds_b[1][i]:
            tmp.append(bds_a[1][i])
        else:
            tmp.append(bds_b[1][i])

    new_bounds.append(tuple(tmp))

    return new_bounds


def check_bounds_and_get_dimension(bounds):

    if type(bounds) not in [tuple, list]:
        raise ValueError

    if len(bounds) != 2:
        raise ValueError

    if len(bounds[0]) != len(bounds[0]):
        raise ValueError

    return len(bounds[0])

