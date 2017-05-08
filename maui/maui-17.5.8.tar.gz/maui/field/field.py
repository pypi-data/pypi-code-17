# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.backend import context
from maui.mesh.prototypes import Mesh
from numpy import ndarray, newaxis, meshgrid, asarray
from maui.backend.prototypes.helper import create_mask_from_indices
import operator
import warnings

class Field(object):

    def __init__(self, partition, name, unit, rank, bounds=None):
        """ Field prototype class.

        :param partition: Partition or Mesh, coordinate space associated with the field.
        :param name: String, unique name of the field/variable.
        :param unit: String, physical unit associated with the field.
        :param rank: Interger, rank of the field.
        :param interpolation: Interpolator, class to obtain value from the field by coordinate.
        :param bounds: 2-Tuple of Tuples, bounds of the field inside the mesh.

        """

        self.__rank = rank
        self.__name = name
        self.__unit = unit

        if isinstance(partition, Mesh):
            partition = context.create_partition(partition, bounds)
        elif bounds is not None:
            partition = partition.copy(bounds)

        self.__partition = partition
        self.__bounds = self.partition.bounds

        #create mask to get Magic Members work with field with bounds not equal mesh bounds
        self.__start_index = self.__partition.mesh.nearest_node(self.__bounds[0])[0]
        self.__stop_index = self.__partition.mesh.nearest_node(self.__bounds[1])[0]

        tmp = list(self.__stop_index)
        for i in range(len(tmp)):
            tmp[i] += 1
        self.__stop_index = tuple(tmp)

        self.__mask = create_mask_from_indices((self.__start_index, self.__stop_index))

        self.__domain_data = context.setup_domain_data(partition, rank)
        self.__d = self.__domain_data.d  # Dict of low level data stores

        self.__interpolator = dict()

        for key in self.__d.keys():
            # TODO: Works only for scalar field, should work for vector and tensor also!
            self.__interpolator[key] = list()

            for i in range(self.partition.mesh.dimension**rank):

                if rank == 0:
                    data = self.__d[key]
                else:
                    data = self.__d[key][i,:]

                #mesh = self.partition.domains[key].mesh
                #x, y, z = meshgrid(mesh.axes[0], mesh.axes[1], mesh.axes[2])
                #points = asarray((x.ravel(order='F'), y.ravel(order='F'), z.ravel(order='F')))

                self.__interpolator[key].append(self.partition.domains[key].mesh.interpolator(self.partition.domains[key].mesh.axes, data))
                #self.__interpolator[key].append(self.partition.domains[key].mesh.interpolator(points.T, data.ravel(order='F')))

    def __getitem__(self, index):
        return self.__domain_data[index]

    def __setitem__(self, index, data):
        self.__domain_data[index] = data

    @property
    def bounds(self):
        return self.__bounds

    @property
    def partition(self):
        return self.__partition

    @property
    def rank(self):
        return self.__rank

    @property
    def name(self):
        return self.__name

    @property
    def unit(self):
        return self.__unit

    def get_value_by_point(self, point):

        tmp = list()
        for i in range(self.partition.mesh.dimension**self.rank):
            for key in self.__interpolator.keys():
                try:
                    tmp.append(self.__interpolator[key][i](point))

                except ValueError:
                    warnings.warn("The given point is out of mesh bounds!")

        if len(tmp) == self.partition.mesh.dimension**self.rank:
            return tmp
        else:
            return None

    def cross_mesh_field_evaluation(self, target_field):

        #if target_field.rank != self.rank:
        #    raise ValueError("Rank of target field should by the same as host field!")

        if len(target_field.d.keys()) <= len(self.__interpolator.keys()):
            key_list = target_field.d.keys()
        else:
            key_list = self.__interpolator.keys()

        for i in range(self.partition.mesh.dimension**self.rank):
            for key in key_list:
                mesh = target_field.partition.domains[key].mesh
                x, y, z = meshgrid(mesh.axes[0], mesh.axes[1], mesh.axes[2], indexing='ij')
                points = asarray((x.ravel(order='F'), y.ravel(order='F'), z.ravel(order='F')))

                if self.rank == 0:
                    try:
                        target_field.d[key].ravel(order='F')[:] = self.__interpolator[key][i](points.T)[:]

                    except ValueError:
                        warnings.warn("One of the given points is out of mesh bounds!")

                else:
                    try:
                        target_field.d[key][i, :] = self.__interpolator[key][i](points.T).reshape(target_field.d[key].shape[1:], order='F')[:]
                    except ValueError:
                        warnings.warn("One of the given points is out of mesh bounds!")

    @property
    def data(self):
        """ Enhanced data property.
        :return: Returns the associated DataPartition
        """
        return self.__domain_data

    @property
    def d(self):
        """ Primitive data property.
        :return: dict() of numpy.ndarrays with the keys of the dict being the coordinate of the corresponding Domain
        """
        return self.__d

    @d.setter
    def d(self, ddict):
        self.__d = ddict

    def sync(self):
        self.__domain_data.sync()

    def __add__(self, x):
        '''Addition with numpy.ndarray or Field (same shape and Partitions) or single number
        :return: dict (same shape as field)
        '''
        return self.__math(operator.add, x)

    def __radd__(self, x):
        '''reverse Addition with single number (does NOT work with np.ndarray!!!)
        :return: dict (same shape as field)
        '''
        return self.__rmath(operator.add, x)

    def __iadd__(self, x):

        for i in self.d: self.__d[i][:] = self.__add__(x)[i][:]
        return self

    def __sub__(self, x):
        '''Subtraction with numpy.ndarray or Field (same shape and Partitions) or single number
        :return: dict (same shape as field)
        '''
        return self.__math(operator.sub, x)

    def __rsub__(self, x):
        '''reverse subtraction with single number (does NOT work with np.ndarray!!!)
        :return: dict (same shape as field)
        '''
        return self.__rmath(operator.sub, x)

    def __isub__(self, x):

        for i in self.d: self.__d[i][:] = self.__sub__(x)[i][:]
        return self

    def __mul__(self, x):
        '''Multiplication with numpy.ndarray or Field (same shape and Partitions) or single number
        :return: dict (same shape as field)
        '''
        return self.__math(operator.mul, x)

    def __rmul__(self, x):
        '''reverse multiplication with single number (does NOT work with np.ndarray!!!)
        :return: dict (same shape as field)
        '''
        return self.__rmath(operator.mul, x)

    def __imul__(self, x):

        for i in self.d: self.__d[i] = self.__mul__(x)[i]
        return self


    def __div__(self, x):
        '''Division with numpy.ndarray or Field (same shape and Partitions) or single number
        :return: dict (same shape as field)
        '''
        return self.__math(operator.div, x)

    def __rdiv__(self, x):
        '''reverse Division with single number (does NOT work with np.ndarray!!!)
        :return: dict (same shape as field)
        '''
        return self.__rmath(operator.div, x)

    def __idiv__(self, x):

        for i in self.d: self.__d[i][:] = self.__div__(x)[i][:]
        return self

    def __truediv__(self, x):

        return self.__div__(x)

    def __rtruediv__(self, x):

        return self.__rdiv__(x)

    def __itruediv__(self, x):

        return self.__idiv__(x)

    def __pow__(self, x):
        '''Power with numpy.ndarray or Field (same shape and Partitions) or single number
        :return: dict (same shape as field)
        '''
        return self.__math(operator.pow, x)

    def __rpow__(self, x):
        '''reverse Power with single number (does NOT work with np.ndarray!!!)
        :return: dict (same shape as field)
        '''
        return self.__rmath(operator.pow, x)

    def __ipow__(self, x):

        for i in self.d: self.__d[i][:] = self.__pow__(x)[i][:]
        return self

    def __mod__(self, x):
        '''Modulo with numpy.ndarray or Field (same shape and Partitions) or single number
        :return: dict (same shape as field)
        '''
        return self.__math(operator.mod, x)

    def __rmod__(self, x):
        '''reverse modulo with single number (does NOT work with np.ndarray!!!)
        :return: dict (same shape as field)
        '''
        return self.__rmath(operator.mod, x)

    def __imod__(self, x):

        for i in self.d: self.__d[i][:] = self.__mod__(x)[i][:]
        return self

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

    #defines operator function
    def __math(self, f, x):
        """operator function
        :param f: operator.add/sub/mul... used operator
        :param x: other object field should be add/sub... with
        :return: dictionary (same shape as field.d) with result of operation
        """

        d = {}
        if isinstance(x, (int, long, float, complex)):
            for i in self.__d: d[i] = f(self.__d[i], x)
        #Operation with other Field or View (same shape, partitions, bounds)
        elif isinstance(x, Field) or isinstance(x, View):
            try:
                for i in x.d: d[i] = f(self.__d[i], x.d[i])
            except: raise ValueError('Fields have to be partitioned in the same way and have same shape to be add/sub/mul/div/pow/mod\nView has to have same bounds and origin mesh as Field.')
        elif isinstance(x, ndarray):
            #array has to be of the same Size as Field
            try:
                for i in self.d:
                    #generate Indices if Field has bounds different from mesh-bounds
                    ind = self.__indices(self.__partition.meta_data[i], self.__mask)
                    d[i] = f(self.d[i], x[ind])
                return d
            except: raise ValueError('Array has to have same shape as Field for operation')
        else: raise ValueError('Operators only available for Field and (Field, numpy.ndarray with same shape as whole Field, integer, float, complex, View).')

        return d

    def __rmath(self, f, x):
        """reverse operator function
        :param f: operator.add/sub/mul... used operator
        :param x: other object field should be add/sub... with
        :return: dictionary (same shape as field.d) with result of operation
        """

        d = {}
        if isinstance(x, (int, long, float, complex)):
            for i in self.__d: d[i] = f(x , self.__d[i])
        else: raise ValueError('Cannot execute reverse operator, only (int, float, complex) as first operand possible')

        return d

    def __array_op(self, f, x, axis):
        """operation for 3D Field with planes or vector (type = numpy.ndarray) or 2D Field with vector (numpy.ndarray)
        :param f: operator function
        :param x: array(1D, 2D) or field (2D) or View (2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """
        if isinstance(x, ndarray) == False and isinstance(x, Field) == False and isinstance(x, View) == False:
            raise ValueError('first argument has to be an array of dimension 1 or 2 or an Field or an View of dimension 2')

        d = {}
        #x is a vector (only numpy ndarray)
        if isinstance(axis, int) and isinstance(x, ndarray):
            if len(self.__partition.mesh.bounds[0]) == 3:

                try:

                    for i in self.__d:
                        try:
                            ind = self.__indices(self.partition.meta_data[i], self.__mask)
                        except:
                            raise ValueError("Indices geht nicht.")

                        if axis == 0:
                            d[i] = f(self.__d[i], x[ind[0]][:, newaxis, newaxis])
                        elif axis == 1:
                            d[i] = f(self.__d[i], x[ind[1]][:, newaxis])
                        elif axis == 2:
                            d[i] = f(self.__d[i], x[ind[2]])
                        else:
                            raise ValueError('"axis" can only have value 0, 1 or 2 .')
                        self.__d[i][:] = d[i][:]
                except:
                    raise ValueError('Vector does not have same length as Field along axis %d.' %axis)
            elif len(self.__partition.mesh.bounds[0]) == 2:
                try:
                    for i in self.__d:
                        ind = self.__indices(self.partition.meta_data[i], self.__mask)
                        if axis == 0:
                            d[i] = f(self.__d[i], x[ind[0]][:, newaxis])
                        elif axis == 1:
                            d[i] = f(self.__d[i], x[ind[1]][:])
                        else:
                            raise ValueError('"axis" can only have value 0 or 2 .')
                        self.__d[i][:] = d[i][:]
                except: raise ValueError('Vector does not have same length as Field along axis %d.' %axis)
        #x is a plane (2D-numpy.ndarray or 2D field or View with same partitions, shape and bounds in plane as 3D field)
        elif len(axis) == 2:
            #operation for 2D-arrays
            if isinstance(x, ndarray):
                try:
                    for i in self.__d:
                        ind = self.__indices(self.partition.meta_data[i], self.__mask)
                        if axis == (0, 1) or axis == (1, 0):
                            d[i] = f(self.__d[i], x[ind[0], ind[1]][:, :, newaxis])
                        elif axis == (1, 2) or axis == (2, 1):
                            d[i] = f(self.__d[i], x[ind[1], ind[2]])
                        elif axis == (0, 2) or axis == (2, 0):
                            d[i] = f(self.__d[i], x[ind[0], ind[2]][:, newaxis, :])
                        else:
                            raise ValueError('Axis-tuple can only contain 0 (x-axis), 1 (y-axis) and 2 (z-axis).')
                        self.__d[i][:] = d[i][:]
                except: raise ValueError('2D-Array does not fit to plane %s of Field' %(axis,))
            #operation for 2D Fields or View (Field from same origin mesh but bounds like View has)
            elif isinstance(x, Field) or isinstance(x, View):
                if axis == (0, 1) or axis == (1, 0):
                    try:
                        for i in self.__d: d[i] = f(self.__d[i], x.d[(i[0],i[1])][:, :, newaxis])
                    except: raise ValueError('2D-Field/-View does not fit to field in xy-plane (maybe whole shape or partitions does not fit)')
                elif axis == (1, 2) or axis == (2, 1):
                    try:
                        for i in self.__d: d[i] = f(self.__d[i], x.d[(i[1],i[2])])
                    except: raise ValueError('2D-Field/-View does not fit to field in yz-plane (maybe whole shape or partitions does not fit)')
                elif axis == (0, 2) or axis == (2, 0):
                    try:
                        for i in self.__d: d[i] = f(self.__d[i], x.d[(i[0],i[2])][:, newaxis, :])
                    except: raise ValueError('2D-Field/-View does not fit to field in xz-plane (maybe whole shape or partitions does not fit)')
                else: raise ValueError('Axis-tuple can only contain 0 (x-axis), 1 (y-axis) and 2 (z-axis).')
            else: raise ValueError('x has to be an Field, View or numpy.ndarray with 2 dimensions (or an 1D numpy.ndarray (vector))')

        else: raise ValueError('Argument "axis" has to be an integer (for vector) or tuple of length 2 (for 2D array or field)')

        return d

    def add(self, x, axis):
        """Function to add 3D field with vector or 2D array (type = numpy.ndarray or 2D Field) or 2D Field with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """

        return self.__array_op(operator.add, x, axis)

    def sub(self, x, axis):
        """Function to sub vector or 2D array (type = numpy.ndarray or 2D Field or View) from 3D field or 2D Field with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """
        return self.__array_op(operator.sub, x, axis)

    def mul(self, x, axis):
        """Function to mul vector or 2D array (type = numpy.ndarray or 2D Field or View) with 3D field or 2D Field with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """
        return self.__array_op(operator.mul, x, axis)

    def div(self, x, axis):
        """Function to div 3D field by vector or 2D array (type = numpy.ndarray or 2D Field or View) or 2D Field with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """
        return self.__array_op(operator.div, x, axis)

    def mod(self, x, axis):
        """Function to modulo 3D field by vector or 2D array (type = numpy.ndarray or 2D Field or View) or 2D Field with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """
        return self.__array_op(operator.mod, x, axis)

    def pow(self, x, axis):
        """Function have a vector or 2D array (type = numpy.ndarray or 2D Field or View) as power of 3D field or 2D Field with vector (type = numpy.ndarray)
        :param x: array(1D, 2D) or field (2D) or View(2D)
        :param axis: specifies axis, eg. axis = (1,2) plane lies in yz-plane, axis=0 vector along x axis
        :return: dict with result of operation (same form as field.d)
        """
        return self.__array_op(operator.pow, x, axis)
