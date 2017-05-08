# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'christoph.statz <at> tu-dresden.de'

from .prototypes import Mesh


class UnstructuredMesh(Mesh):

    def __init__(self, vertices, lines=None, faces=None, cells=None, axes_names=('x', 'y', 'z'), unit='m'):
        """ UnstructuredMesh defined by a list of vertices (points) and one of {lines, faces, cells}.

        :param vertices: list of vertices.
        :param lines: List of lines.
        :param faces: List of faces.
        :param cells: List of cells.
        :param axes_names: Type of coordinate system.
        :param unit: Unit of mesh values.
        """

        # TODO: Compute bounds from vertices!
        # TODO: call super class constructor
        # Mesh.__init__(self, bounds, axes_names=axes_names, unit=unit, context=context)

        self._vertices = vertices
        self._lines = lines
        self._faces = faces
        self._cells = cells

    @property
    def vertices(self):
        return self._vertices

    @property
    def lines(self):
        return self._lines

    @property
    def faces(self):
        return self._faces

    @property
    def cells(self):
        return self._cells
