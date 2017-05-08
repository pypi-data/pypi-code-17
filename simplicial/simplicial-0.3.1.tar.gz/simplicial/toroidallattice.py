# Toroidal lattices, a plane folded to have a hole
#
# Copyright (C) 2017 Simon Dobson
# 
# This file is part of simplicial, simplicial topology in Python.
#
# Simplicial is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Simplicial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Simplicial. If not, see <http://www.gnu.org/licenses/gpl.html>.

from simplicial import *

class ToroidalLattice(SimplicialComplex):

    '''The simplcest simplicial lattice defining a torus, a cylinder whose
    ends are connected.'''
    
    def __init__( self ):
        '''Create a toroid.'''
        super(ToroidalLattice, self).__init__()
        
        # add the basis
        for i in range(4):
            for j in range(4):
                self.addSimplex(id = self._indexOfVertex(i, j))

        # add the EW edges
        for i in range(4):
            for j in range(3):
                self.addSimplexWithBasis([ self._indexOfVertex(i, j),
                                           self._indexOfVertex(i, j + 1) ])
        # add the NS edges
        for i in range(3):
            for j in range(4):
                self.addSimplexWithBasis([ self._indexOfVertex(i, j),
                                           self._indexOfVertex(i + 1, j) ])

        # add the triangles
        for i in range(3):
            for j in range(3):
                self.addSimplexWithBasis([ self._indexOfVertex(i, j),
                                           self._indexOfVertex(i, j + 1),
                                           self._indexOfVertex(i + 1, j) ])
                self.addSimplexWithBasis([ self._indexOfVertex(i + 1, j + 1),
                                           self._indexOfVertex(i, j + 1),
                                           self._indexOfVertex(i + 1, j) ])

    def _indexOfVertex( self, i, j ):
        '''Return the identifier of the given (row, column) vertex (0-simplex).
        Row and column indexing start from zero.
        
        :param i: the row
        :param j: the column
        :returns: the identifier of the point'''
        return i * 4 + j
