# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.backend.prototypes.helper import create_mask_from_indices
from numpy import ndarray, newaxis
import operator
from maui.field.field import Field


class View(Field):

    def __init__(self, field, partition=None, bounds=None):
        """ View prototype class.

        :param partition: Partition or Mesh, coordinate space associated with the field.
        :param name: String, unique name of the field/variable.
        :param unit: String, physical unit associated with the field.
        :param rank: Integer, rank of the field.
        :param interpolation: Interpolator, class to obtain value from the field by coordinate.
        :param bounds: 2-Tuple of Tuples, bounds of the field inside the mesh.

        """

        self.__field = field

        if partition is None:
            self.__partition = self.__field.partition.copy(bounds=bounds)
        else:
            self.__partition = partition.copy(bounds=bounds)

        self.__bounds = bounds
        self.__domain_data = self.__field.data
        self.__d = self.__field.data.d  # Dict of low level data stores

        self.__start_index = self.__partition.mesh.nearest_node(bounds[0])[0]
        self.__stop_index = self.__partition.mesh.nearest_node(bounds[1])[0]

        tmp = list(self.__stop_index)

        for i in range(len(tmp)):
            tmp[i] += 1

        self.__stop_index = tuple(tmp)

        self.__mask = create_mask_from_indices((self.__start_index, self.__stop_index))

    def __getitem__(self, index):
        # Mask
        # Only check bounds using start and stop index!
        return self.__domain_data[index]

    def __setitem__(self, index, data):
        # Mask
        # Only check bounds!
        self.__domain_data[index] = data

    @property
    def bounds(self):
        return self.__bounds

    @property
    def partition(self):
        return self.__partition

    @property
    def rank(self):
        return self.__field.rank

    @property
    def name(self):
        return self.__field.name

    @property
    def unit(self):
        return self.__field.unit

    @property
    def interpolation(self):
        return self.__field.interpolation

    @property
    def d(self):
        """ Primitive data property.
        :return: dict() of numpy.ndarrays with the keys of the dict being the coordinate of the corresponding Domain
        """
        return self.__field[self.__mask]

    def sync(self):
        self.__domain_data.sync()

    def __indices(self, slice_partition, slice_mask):
        #function to generate Indices for operations with Array and Field with bounds different from mesh bounds
        ind=[]
        for j in xrange(len(slice_partition)):
            if slice_partition[j].start <= slice_mask[j].start:
                start = None
            else:
                start = slice_partition[j].start - slice_mask[j].start
            if slice_partition[j].stop >= slice_mask[j].stop:
                stop = None
            else:
                stop = slice_partition[j].stop - slice_mask[j].start
            ind.append(slice(start, stop, None))
        return tuple(ind)

    def __math(self, f, x):
        """operator function
        :param f: operator.add/sub/mul... used operator
        :param x: other object view should be add/sub... with (other View, number, numpy.ndarray, Field)
        :return: dictionary (same shape as field.d) with result of operation
        """

        d = {}
        #operation with single number
        if isinstance(x, (int, long, float, complex)):
            for i in self.d: d[i] = f(self.d[i], x)
            return d
        #operation with other view (must have same size and partitions as self) or Field from same mesh and same bounds like View
        elif isinstance(x, View) or isinstance(x, Field):
            try:
                for i in self.d:
                    d[i] = f(self.d[i], x.d[i])
                return d
            except: raise ValueError('Views have to be partitioned and shaped in the same way to be add/sub/mul/div/pow/mod\nField has to have same bounds and origin mesh as View.')
        #operation with numpy array
        elif isinstance(x, ndarray):
            #array has to be of the same Size as View
            try:
                for i in self.d:
                    ind = self.__indices(self.__partition.meta_data[i], self.__mask)
                    d[i] = f(self.d[i], x[ind])
                return d
            except: raise ValueError('Array has to have same shape as View for operation')

        else: raise ValueError('Operators only available for View and (View, Field, numpy.ndarray with same shape View, integer, float, complex).')

    def __add__(self, x):
        return self.__math(operator.add, x)

    def __radd__(self, x):
        return self.__math(operator.add, x)

    def __iadd__(self, x):
        for i in self.d: self.d[i][:] = self.__add__(x)[i][:]
        return self

    def __sub__(self, x):
        return self.__math(operator.sub, x)

    def __rsub__(self, x):
        return self.__math(operator.sub, x)

    def __isub__(self, x):
        for i in self.d: self.d[i][:] = self.__sub__(x)[i][:]
        return self

    def __mul__(self, x):
        return self.__math(operator.mul, x)

    def __rmul__(self, x):
        return self.__math(operator.mul, x)

    def __imul__(self, x):
        for i in self.d: self.d[i][:] = self.__mul__(x)[i][:]
        return self

    def __div__(self, x):
        return self.__math(operator.div, x)

    def __rdiv__(self, x):
        return self.__math(operator.div, x)

    def __idiv__(self, x):
        for i in self.d: self.d[i][:] = self.__div__(x)[i][:]
        return self

    def __truediv__(self, x):
        return self.__div__(x)

    def __rtruediv__(self, x):
        return self.__div__(x)

    def __itruediv__(self, x):
        for i in self.d: self.d[i][:] = self.__truediv__(x)[i][:]
        return self

    def __mod__(self, x):
        return self.__math(operator.mod, x)

    def __rmod__(self, x):
        return self.__math(operator.mod, x)

    def __imod__(self, x):
        for i in self.d: self.d[i][:] = self.__mod__(x)[i][:]
        return self

    def __pow__(self, x):
        return self.__math(operator.pow, x)

    def __rpow__(self, x):
        return self.__math(operator.pow, x)

    def __ipow__(self, x):
        for i in self.d: self.d[i][:] = self.__pow__(x)[i][:]
        return self


    def __array_op(self, f, x, axis):
        """operation for 3D Field with planes or vector (type = numpy.ndarray) or 2D Field with vector (numpy.ndarray)
        :param f: operator function
        :param x: array(1D, 2D) or field (2D) or View (2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """
        if isinstance(x, ndarray) == False and isinstance(x, Field) == False and isinstance(x, View) == False:
            raise ValueError('first argument has to be an array of dimension 1 or 2 or an Field or an View of dimension 2')

        d ={}
        #x is a vector (only numpy ndarray)
        if isinstance(axis, int) and isinstance(x, ndarray):
            if len(self.__partition.mesh.bounds[0]) == 3:
                try:
                    for i in self.d:
                        ind = self.__indices(self.partition.meta_data[i], self.__mask)
                        if axis == 0:
                            d[i] = f(self.d[i], x[ind[0]][:, newaxis, newaxis])
                        elif axis == 1:
                            d[i] = f(self.d[i], x[ind[1]][:, newaxis])
                        elif axis == 2:
                            d[i] = f(self.d[i], x[ind[2]])
                        else:
                            raise ValueError('"axis" can only have value 0, 1 or 2 .')
                except: raise ValueError('Vector does not have same length as Field along axis %d.' %axis)
            elif len(self.__partition.mesh.bounds[0]) == 2:
                try:
                    for i in self.d:
                        ind = self.__indices(self.partition.meta_data[i], self.__mask)
                        if axis == 0:
                            d[i] = f(self.d[i], x[ind[0]][:, newaxis])
                        elif axis == 1:
                            d[i] = f(self.d[i], x[ind[1]][:])
                        else:
                            raise ValueError('"axis" can only have value 0 or 2 .')
                except: raise ValueError('Vector does not have same length as Field along axis %d.' %axis)
        #x is a plane (2D-numpy.ndarray or 2D field or View with same partitions, shape and bounds in plane as 3D field)
        elif len(axis) == 2:
            #operation for 2D-arrays
            if isinstance(x, ndarray):
                try:
                    for i in self.d:
                        ind = self.__indices(self.partition.meta_data[i], self.__mask)
                        if axis == (0, 1) or axis == (1, 0):
                            d[i] = f(self.d[i], x[ind[0], ind[1]][:, :, newaxis])
                        elif axis == (1, 2) or axis == (2, 1):
                            d[i] = f(self.d[i], x[ind[1], ind[2]])
                        elif axis == (0, 2) or axis == (2, 0):
                            d[i] = f(self.d[i], x[ind[0], ind[2]][:, newaxis, :])
                        else:
                            raise ValueError('Axis-tuple can only contain 0 (x-axis), 1 (y-axis) and 2 (z-axis).')
                except: raise ValueError('2D-Array does not fit to plane %s of Field' %(axis,))
            #operation for 2D Fields or View (Field from same origin mesh but bounds like View has)
            elif isinstance(x, Field) or isinstance(x, View):
                if axis == (0, 1) or axis == (1, 0):
                    try:
                        for i in self.d: d[i] = f(self.d[i], x.d[(i[0],i[1])][:, :, newaxis])
                    except: raise ValueError('2D-Field/-View does not fit to field in xy-plane (maybe whole shape or partitions does not fit)')
                elif axis == (1, 2) or axis == (2, 1):
                    try:
                        for i in self.d: d[i] = f(self.d[i], x.d[(i[1],i[2])])
                    except: raise ValueError('2D-Field/-View does not fit to field in yz-plane (maybe whole shape or partitions does not fit)')
                elif axis == (0, 2) or axis == (2, 0):
                    try:
                        for i in self.d: d[i] = f(self.d[i], x.d[(i[0],i[2])][:, newaxis, :])
                    except: raise ValueError('2D-Field/-View does not fit to field in xz-plane (maybe whole shape or partitions does not fit)')
                else: raise ValueError('Axis-tuple can only contain 0 (x-axis), 1 (y-axis) and 2 (z-axis).')
            else: raise ValueError('x has to be an Field, View or numpy.ndarray with 2 dimensions (or an 1D numpy.ndarray (vector))')

        else: raise ValueError('Argument "axis" has to be an integer (for vector) or tuple of length 2 (for 2D array or field)')

        return d

    def add(self, x, axis):
        """Function to add 3D View with vector or 2D array (type = numpy.ndarray or 2D Field or 2D View) or 2D View with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as view.d)
        """
        return self.__array_op(operator.add, x, axis)

    def sub(self, x, axis):
        """Function to sub 3D View with vector or 2D array (type = numpy.ndarray or 2D Field or 2D View) or 2D View with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as view.d)
        """
        return self.__array_op(operator.sub, x, axis)

    def mul(self, x, axis):
        """Function to multiply 3D View with vector or 2D array (type = numpy.ndarray or 2D Field or 2D View) or 2D View with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as view.d)
        """
        return self.__array_op(operator.mul, x, axis)

    def div(self, x, axis):
        """Function to divide 3D View by vector or 2D array (type = numpy.ndarray or 2D Field or 2D View) or 2D View with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as view.d)
        """
        return self.__array_op(operator.div, x, axis)

    def mod(self, x, axis):
        """Function to modulo 3D View with vector or 2D array (type = numpy.ndarray or 2D Field or 2D View) or 2D View with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as view.d)
        """
        return self.__array_op(operator.mod, x, axis)

    def pow(self, x, axis):
        """Function to power 3D View with vector or 2D array (type = numpy.ndarray or 2D Field or 2D View) or 2D View with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as view.d)
        """
        return self.__array_op(operator.pow, x, axis)
