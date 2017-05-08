# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np
from xml.etree import ElementTree as etree
from xml.dom import minidom

from .encoder import Base64EncodedBuffer, Base64ZLibEncodedBuffer
from .vtkdefs import *
from .helper import *


def prettify(elem):
    return minidom.parseString(etree.tostring(elem, 'us-ascii')).toprettyxml(indent="  ")


def appended_data_node(root, data_list):

    attributes=dict()
    attributes['encoding']='base64'
    data = etree.SubElement(root, 'AppendedData', attrib=attributes)

    data.text = '_'

    for elem in data_list:
        data.text += elem

    return data


def point_data_node(root, scalars=None, vectors=None, tensors=None):

    attributes=dict()

    if scalars is not None:
        attributes['scalars'] = scalars
    if vectors is not None:
        attributes['vectors'] = vectors
    if tensors is not None:
        attributes['tensors'] = tensors

    return etree.SubElement(root, 'PointData', attrib=attributes)

def ppoint_data_node(root, scalars=None, vectors=None, tensors=None):

    attributes=dict()

    if scalars is not None:
        attributes['scalars'] = scalars
    if vectors is not None:
        attributes['vectors'] = vectors
    if tensors is not None:
        attributes['tensors'] = tensors

    return etree.SubElement(root, 'PPointData', attrib=attributes)



def time_and_cycle_node(root, cycle, time):

    field_element = etree.SubElement(root, 'FieldData')

    attributes = dict()
    attributes['NumberOfTuples'] = '1'
    attributes['type'] = VTK_FLOAT32
    attributes['format'] = 'ascii'

    if cycle is not None:
        attributes['name'] = 'CYCLE'
        cycle_element = etree.SubElement(field_element, "DataArray", attrib=attributes)
        cycle_element.text = str(cycle)

    if time is not None:
        attributes['name'] = 'TIME'
        time_element = etree.SubElement(field_element, "DataArray", attrib=attributes)
        time_element.text = str(time)

    return field_element


def file_node(file_type, compressed=False):

    attributes = dict()

    if compressed:
        attributes['compressor'] = 'vtkZLibDataCompressor'

    attributes['type'] = file_type
    attributes['version'] = '1.0'
    attributes['byte_order'] = get_vtkfile_byteorder_string()
    attributes['header_type'] = 'UInt64'

    return etree.Element('VTKFile', attrib=attributes)


def piece_node(root, start, stop, source=None):

    attributes=dict()
    attributes['Extent'] = generate_extents_string(start, stop)
    if source is not None:
        attributes['Source'] = source

    return etree.SubElement(root, 'Piece', attrib=attributes)


def data_array_node(root, numberofcomponents=None, offset=None, dtype=None, name=None, format='ascii'):

    attributes=dict()
    if numberofcomponents is not None:
        attributes['NumberOfComponents'] = str(numberofcomponents)

    if offset is not None:
        attributes['offset'] = offset

    if dtype is not None:
        attributes['type'] = numpy_to_vtk_typemap[dtype]

    if name is not None:
        attributes['Name'] = name

    attributes['format'] = format

    return etree.SubElement(root, 'DataArray', attrib=attributes)

def pdata_array_node(root, numberofcomponents=None, offset=None, dtype=None, name=None, format=None):

    attributes=dict()
    if numberofcomponents is not None:
        attributes['NumberOfComponents'] = str(numberofcomponents)

    if offset is not None:
        attributes['offset'] = offset

    if dtype is not None:
        attributes['type'] = numpy_to_vtk_typemap[dtype]

    if name is not None:
        attributes['Name'] = name

    if format is not None:
        attributes['format'] = format

    return etree.SubElement(root, 'PDataArray', attrib=attributes)


def get_vtkfile_byteorder_string():

    import sys

    if sys.byteorder == "little":
        return "LittleEndian"

    return "BigEndian"


def generate_extents_string(start, end):

    assert (len(start) == len(end))

    string = ""

    for i in range(len(start)):

        string += str(start[i]) + ' '
        string += str(end[i]) + ' '

    for i in range(3 - len(start)):
        string += '0 '
        string += '0 '

    return string


class VTRWriter(object):

    def __init__(self, prefix, mesh, data, var_name, var_type, compressed=False):

        self.__compressed = compressed
        self.__mesh = mesh
        self.__data = data
        self.__name = var_name
        self.__type = var_type
        self.__prefix = prefix
        self.__compressed = compressed

    def write(self, cycle=None, time=None):

        vtkfile = self.__file_node()

        if cycle is not None or time is not None:
            time_and_cycle_node(vtkfile, cycle, time)

        offset = 0
        data = []

        start = tuple([0 for axe in self.__mesh.axes])
        stop = tuple([axe.size-1 for axe in self.__mesh.axes])

        grid = self.__rectilinear_grid_node(vtkfile, start, stop)
        piece = piece_node(grid, start, stop)
        coordinates = self.__coordinates_node(piece)

        # add axes
        for i, axe in enumerate(self.__mesh.axes):
            data_array_node(coordinates, numberofcomponents='1', offset=str(offset), dtype=axe.dtype, name=self.__mesh.axes_names[i], format='appended')
            tmp, l = self.__encode(axe)
            offset += l
            data.append(tmp)

        # add dummy axes
        for i in range(3-len(self.__mesh.axes)):
            d = data_array_node(coordinates, numberofcomponents='1', dtype=np.dtype(np.float32), name='z'+str(i), format='ascii')
	    d.text = '0'

        scalars, vectors, tensors = None, None, None
        # add pointdata
        if self.__type == 0:
            scalars = self.__name
        elif self.__type == 1:
            vectors = self.__name
        elif self.__type == 2:
            tensors = self.__name

        point_data = point_data_node(piece, scalars=scalars, vectors=vectors, tensors=tensors)

        dim = len(self.__mesh.axes)
        components = 3**self.__type
        data_array_node(point_data, numberofcomponents=str(components), offset=str(offset), dtype=self.__data.dtype, name=self.__name, format='appended')

        if self.__type == 0 or dim == 3:
            tmp, l = self.__encode(self.__data)
        else:
            s = list(self.__data.shape)

            for i in range(self.__type):
                s[i] = 3

            slc = tuple([slice(0, e) for e in self.__data.shape])

            d = np.zeros(tuple(s), dtype=self.__data.dtype)
            d[slc] = self.__data[None]
            tmp, l = self.__encode(d)

        data.append(tmp)
        offset += l

        if len(data) > 0:
            appended_data_node(vtkfile, data)

        tree = etree.ElementTree(vtkfile)

        filename = self.__prefix + generate_filename(self.__name, cycle) + '.vtr'
        tree.write(filename)

    def __encode(self, data):
        if self.__compressed:
            buf = Base64ZLibEncodedBuffer(buffer(data.astype(data.dtype, order='F', copy=False)))
        else:
            buf = Base64EncodedBuffer(buffer(data.astype(data.dtype, order='F', copy=False)))

        return buf.header + buf.data, len(buf)

    def __file_node(self):
        return file_node('RectilinearGrid', self.__compressed)

    def __rectilinear_grid_node(self, root, start, stop):

        attributes=dict()
        attributes['WholeExtent'] = generate_extents_string(start, stop)

        return etree.SubElement(root, 'RectilinearGrid', attrib=attributes)

    def __coordinates_node(self, root):
        return etree.SubElement(root, 'Coordinates')


class PVTRWriter(object):

    def __init__(self, prefix, mesh, data_dtype, meta_data, var_name, var_type, stencil):

        self.__dtype = data_dtype
        self.__name = var_name
        self.__type = var_type
        self.__prefix = prefix
        self.__mesh = mesh
        self.__meta_data = meta_data

        # ghostlevel needs to be computed correctly!
        # does seem to have no impact in visit.
        self.__ghostlevel = 0


    def write(self, cycle=None, time=None):

        pvtkfile = self.__file_node()

        if cycle is not None or time is not None:
            time_and_cycle_node(pvtkfile, cycle, time)

        start = tuple([0 for axe in self.__mesh.axes])
        stop = tuple([axe.size-1 for axe in self.__mesh.axes])

        pgrid = self.__prectilinear_grid_node(pvtkfile, start, stop)
        pcoordinates = self.__pcoordinates_node(pgrid)

        # add axes
        for i, axe in enumerate(self.__mesh.axes):
            pdata_array_node(pcoordinates, numberofcomponents='1', format='appended', dtype=axe.dtype, name=self.__mesh.axes_names[i])

        # add dummy axes
        for i in range(3-len(self.__mesh.axes)):
            pdata_array_node(pcoordinates, numberofcomponents='1', format='ascii', dtype=np.dtype(np.float32), name='z'+str(i))

        scalars, vectors, tensors = None, None, None
        # add pointdata
        if self.__type == 0:
            scalars = self.__name
        elif self.__type == 1:
            vectors = self.__name
        elif self.__type == 2:
            tensors = self.__name

        ppoint_data = point_data_node(pgrid, scalars=scalars, vectors=vectors, tensors=tensors)

        dim = len(self.__mesh.axes)
        components = 3**self.__type
        pdata_array_node(ppoint_data, numberofcomponents=str(components),  dtype=self.__dtype, name=self.__name)

        for key in self.__meta_data.keys():
            start = tuple([e.start for e in self.__meta_data[key]])
            stop = tuple([e.stop-1 for e in self.__meta_data[key]])
            filename = generate_dirname('./', key) + self.__prefix.split('/')[-1] + generate_filename(self.__name, cycle) +'.vtr'
            piece_node(pgrid, start, stop, source=filename)

        tree = etree.ElementTree(pvtkfile)
        filename = self.__prefix + generate_filename(self.__name, cycle) + '.pvtr'
        tree.write(filename)

    def __file_node(self):
        return file_node('PRectilinearGrid')

    def __prectilinear_grid_node(self, root, start, stop):

        attributes=dict()
        attributes['WholeExtent'] = generate_extents_string(start, stop)
        attributes['GhostLevel'] = str(self.__ghostlevel)

        return etree.SubElement(root, 'PRectilinearGrid', attrib=attributes)

    def __pcoordinates_node(self, root):
        return etree.SubElement(root, 'PCoordinates')
