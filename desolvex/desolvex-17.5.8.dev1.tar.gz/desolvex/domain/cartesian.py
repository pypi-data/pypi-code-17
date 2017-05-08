# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.field import ScalarField
from maui.mesh import CartesianMesh
from copy import deepcopy

from .domain import Domain


class CartesianDomain(Domain):

    def __init__(self, bounds, pitch, fields, variables, coordinates=('x', 'y', 'z'), initializer=None):

        # initialize meshes/discretization
        meshes = dict()

        meshes['node'] = CartesianMesh(bounds, pitch)

        if 'cell' in fields.keys():
            meshes['cell'] = meshes['node'].copy().shift(tuple([pitch/2. for _ in coordinates]))

        if 'edge' in fields.keys():
            meshes['edge'] = dict()
            for i, axis in enumerate(coordinates):
                offset = [0 for _ in coordinates]
                offset[i] = pitch/2.
                meshes['edge'][axis] = meshes['node'].copy().shift(tuple(offset))

        if 'face' in fields.keys():
            meshes['face'] = dict()
            for i, axis in enumerate(coordinates):
                offset = [False for _ in coordinates]
                offset[i] = True
                offset[:] = [not i for i in offset]
                offset[:] = [pitch/2.*i for i in offset]
                meshes['face'][axis] = meshes['node'].copy().shift(tuple(offset))

        Domain.__init__(self, meshes, fields, variables, coordinates, initializer)
