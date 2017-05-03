#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import os

import numpy as np

import joker.aligner


def locate_submat(name):
    d = os.path.split(joker.aligner.__file__)[0]
    p = os.path.join(d, 'matrix', name)
    if not os.path.isfile(p):
        errmsg = 'cannot find substitue matrix "{}"'.format(name)
        raise IOError(errmsg)
    return p


def load_submat(path):
    if '/' not in path:
        path = locate_submat(path)

    with open(path) as infile:
        ichars = []
        jstring = None
        jsize = 0
        scores = []

        for line in infile:
            line = line.strip()
            if line and not line.startswith('#'):
                # remove whitespaces
                jstring = ''.join(line.split())
                jsize = len(jstring) + 1
                break

        if jstring is None:
            raise ValueError('bad substitution matrix')

        for line in infile:
            items = line.split()
            if not items:
                continue

            if len(items) != jsize:
                raise ValueError('bad substitution matrix')
            ichars.append(items[0])
            scores.append([int(s) for s in items[1:]])

    istring = ''.join(ichars)
    submatr = np.array(scores, dtype=int)
    return istring, jstring, submatr


def test():
    p = '/Users/Hailong/Cloud/Imbark/code/jokerseries/joker-aligner/joker/aligner/matrix/blosum30'
    i, j, s = load_submat(p)
    print(i)
    print(j)
    print(s)


if __name__ == '__main__':
    test()
