# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np


# VTK Data Types
VTK_INT8 = "Int8"
VTK_UINT8 = "UInt8"
VTK_INT16 = "Int16"
VTK_UINT16 = "UInt16"
VTK_INT32 = "Int32"
VTK_UINT32 = "UInt32"
VTK_INT64 = "Int64"
VTK_UINT64 = "UInt64"
VTK_FLOAT32 = "Float32"
VTK_FLOAT64 = "Float64"


# VTK Element Types
VTK_VERTEX = 1
VTK_POLY_VERTEX = 2
VTK_LINE = 3
VTK_POLY_LINE = 4
VTK_TRIANGLE = 5
VTK_TRIANGLE_STRIP = 6
VTK_POLYGON = 7
VTK_PIXEL = 8
VTK_QUAD = 9
VTK_TETRA = 10
VTK_VOXEL = 11
VTK_HEXAHEDRON = 12
VTK_WEDGE = 13
VTK_PYRAMID = 14


# VTK Element Node Counts
CELL_NODE_COUNT = {
        VTK_VERTEX: 1,
        VTK_LINE: 2,
        VTK_TRIANGLE: 3,
        VTK_PIXEL: 4,
        VTK_QUAD: 4,
        VTK_TETRA: 4,
        VTK_VOXEL: 8,
        VTK_HEXAHEDRON: 8,
        VTK_WEDGE: 6,
        VTK_PYRAMID: 5,
        }


# numpy to VTK type map
numpy_to_vtk_typemap = dict()
numpy_to_vtk_typemap[np.dtype(np.int8)] = VTK_INT8
numpy_to_vtk_typemap[np.dtype(np.uint8)] = VTK_UINT8
numpy_to_vtk_typemap[np.dtype(np.int16)] = VTK_INT16
numpy_to_vtk_typemap[np.dtype(np.uint16)] = VTK_UINT16
numpy_to_vtk_typemap[np.dtype(np.int32)] = VTK_INT32
numpy_to_vtk_typemap[np.dtype(np.uint32)] = VTK_UINT32
numpy_to_vtk_typemap[np.dtype(np.int64)] = VTK_INT64
numpy_to_vtk_typemap[np.dtype(np.uint64)] = VTK_UINT64
numpy_to_vtk_typemap[np.dtype(np.float32)] = VTK_FLOAT32
numpy_to_vtk_typemap[np.dtype(np.float64)] = VTK_FLOAT64