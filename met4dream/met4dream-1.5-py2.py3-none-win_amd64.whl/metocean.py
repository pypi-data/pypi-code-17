# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:28:44 2016

@author: Øivin Aarnes
@email: oivin.aarnes@dnvgl.com
@version: 1.3
@environment: Python 2.7 for Windows 64-bit
@dependencies: netCDF Operators (NCO) for Python, netCDF4 Python interface to the netCDF C library, Numerical Python for scientific computing

@description:
    Classes to work with netcdf metocean archives of ROMS-Norkyst800m
    * Subset netcdf files
    * Concatenate netcdf files
    * Write netcdf files
    * Extract current vector field

@credits: MET Norway, http://thredds.met.no/thredds/fou-hi/norkyst800m.html

"""
from netCDF4 import Dataset
from nco import Nco, custom, NCOException
from netcdftime import utime
import glob, numpy as np

class location:

    def __init__(self, dataset, coordinates, angle_grid):
        self.dataset = dataset
        self.angle_grid = angle_grid
        self._x = coordinates['x']
        self._y = coordinates['y']
        self._longitude = 0
        self._latitude = 0
        self.has_index = False
        self.has_angle = False
        self.within_bounds = False
        self.xi = None
        self.yi = None
        self.angle = None

        self.initialize()

    def check_is_within_bounds(self, variable, value):
        within_bounds = (variable.min() <= value <= variable.max())
        return within_bounds

    # find index of nearest value
    def lookup_index(self, variable, value):
        index = (np.abs(variable - value)).argmin()
        return index

    # lookup grid convergence angle at location
    def lookup_grid_convergence_angle(self, xi, yi):
        angle = Dataset(self.angle_grid).variables['angle'][yi, xi]
        return angle

    def initialize(self):
        d = Dataset(self.dataset)
        X = d.variables['X']
        Y = d.variables['Y']
        x = X[:]
        y = Y[:]

        valid_x = self.check_is_within_bounds(x, self._x)
        valid_y = self.check_is_within_bounds(y, self._y)
        self.within_bounds = (valid_x and valid_y)

        if self.within_bounds:
            self.xi = self.lookup_index(x, self._x)
            self.yi = self.lookup_index(y, self._y)
            self.has_index = True

            if self.angle_grid:
                self.angle = self.lookup_grid_convergence_angle(self.xi, self.yi)
                self.has_angle = True
        d.close()

    def is_valid(self):
        return (self.within_bounds and self.has_index and self.has_angle)


class netcdf:

    def __init__(self):
        self.xi = None
        self.yi = None
        self.hasIndices = False
        self.nco = Nco()

    def set_indices(self, xi, yi):
        if len(xi) == 0 or len(yi) == 0:
            raise IndexError('Invalid extent or area is out of bounds!')
        self.xi = xi
        self.yi = yi
        self.hasIndices = True

    def filter_indices(self, source, bbox):
        i = Dataset(source)
        X = i.variables['X']
        Y = i.variables['Y']
        x = X[:]
        y = Y[:]
        i.close()

        xi = self.query_indices(x, bbox['xmin'], bbox['xmax'])
        yi = self.query_indices(y, bbox['ymin'], bbox['ymax'])
        self.set_indices(xi, yi)

    def hyperslab(self, source, sink, bbox):
        if not self.hasIndices:
            self.filter_indices(source, bbox)
        _input = source
        _output = sink
        _options = [
            custom.Limit('X', self.xi.min(), self.xi.max()),
            custom.Limit('Y', self.yi.min(), self.yi.max())
        ]
        self.nco.ncks(input=_input, output=_output, options=_options)

    def query_indices(self, variable, _min, _max):
        indices = np.where((variable > _min) & (variable < _max))[0]
        return indices

    def hyperslab_variable(self, variable, yi, xi, source, target):
        x = source.variables[variable]
        _x = target.createVariable(variable, x.dtype, x.dimensions)
        self.copy_ncattr(x, _x)
        _x[:] = x[:, :, yi, xi]

    def copy_ncattr(self, a, b):
        for attr in a.ncattrs():
            b.setncattr(attr, a.getncattr(attr))


class archive:

    def __init__(self, source, sink):
        self.source = source
        self.sink = sink

        # instantiate netcdf operators
        self.nco = Nco()
        self.kitchen_sink()

    def kitchen_sink(self):
        # prepare files for concatination
        for f in self.source:
            o = self.sink + '/' + f
            # make time record dimension to aggregate upon
            self.nco.ncks(input=f, output=o, options='--mk_rec_dmn time')

    def check_integrity(self, files):
        # checking depth dimension is consistent across all files
        a = []
        for r in files:
            d = Dataset(r)
            n = len(d.dimensions['depth'])
            a.append(n)
            d.close()
        b = np.array(a)
        c = (b == a[0])
        return c

    def aggregate(self, prefix, year, month, out):
        try:
            mm = str(month).zfill(2)
            wc = self.sink + '/{0}.{1}{2}*'.format(prefix, year, mm)
            files = glob.glob(wc)

            if len(files) > 0:
                files_consistent = self.check_integrity(files)
                if not files_consistent.all():
                    print('--- The depth dimension varies across files. Check files for consistency!')

                # ensure consistent files
                a = np.array(files)
                b = a[files_consistent]

                # concatinate files on time dimension
                self.nco.ncrcat(input=b, output=out)
                return True
            return False

        except (NCOException) as e:
            print ('Aggregation failed! Check files. ' + e)


class utils:

    def __init__(self):
        self.functions = ['convert nc time']

    def num2date(self, variable, index):
        value = variable[index]
        units = variable.units
        ut = utime(units)
        date = ut.num2date(value)
        return date
