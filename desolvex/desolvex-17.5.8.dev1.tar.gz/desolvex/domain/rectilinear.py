# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.field import ScalarField
from maui.mesh import RectilinearMesh
from copy import deepcopy

from .domain import Domain


class RectilinearDomain(Domain):

    def __init__(self, axes, fields, variables, coordinates=('x', 'y', 'z'), initializer=None):

        # initialize meshes/discretization
        meshes = dict()

        meshes['node'] = RectilinearMesh(axes)
        axes_ext = [np.zeros(axe.size) for axe in axes]
        for k, axe in enumerate(axes_ext):
            axe[:-1] = (axes[k][1:]+axes[k][:-1])/2.
            axe[-1] = 2.*axes[k][-1] - axes[k][-1]

        if 'cell' in fields.keys():
            meshes['cell'] = RectilinearMesh(axes_ext) 

        if 'edge' in fields.keys():
            meshes['edge'] = dict()
            for i, axis in enumerate(coordinates):
                axes_edge = deepcopy(axes)
                axes_edge[i] = axes_ext[i].copy()
                meshes['edge'][axis] = RectilinearMesh(axes_edge)

        if 'face' in fields.keys():
            meshes['face'] = dict()
            for i, axis in enumerate(coordinates):
                offset = [False for _ in coordinates]
                offset[i] = True
                offset[:] = [not i for i in offset]
                axes_face = [axe.copy for axe in axes]

                for k, truth in enumerate(offset):
                    if truth: axes_face[k] = axes_ext[k].copy()

                meshes['face'][axis] = RectilinearMesh(axes_face)

        Domain.__init__(self, meshes, fields, variables, coordinates, initializer)
