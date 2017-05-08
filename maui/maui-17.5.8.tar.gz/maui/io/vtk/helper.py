# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from os import makedirs


def create_dirs(prefix, fields):
    for field in fields:
        for coordinate in field.partition.domains.keys():
            try:
                makedirs(generate_dirname(prefix, coordinate))
            except OSError:
                pass


def generate_dirname(prefix, coordinate):

    tmp = ''

    for i, k  in enumerate(coordinate):
        tmp += str(k)
        if i < len(coordinate)-1:
            tmp += '_'
        dirname = prefix + tmp + '/'
    return dirname


def generate_filename(name, cycle, digits=5):

    filename = '_'+name

    if cycle is not None:
        template = '_%0' + str(digits) + 'd'
        filename += template % int(cycle)

    return filename