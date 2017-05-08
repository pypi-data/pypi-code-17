# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.backend import context
from maui.mesh import RectilinearMesh
from maui.field import ScalarField

from .writer import VTRWriter, PVTRWriter
from .helper import create_dirs, generate_dirname, generate_filename


class VTKOutput(object):

    def __init__(self, fields, identifier, prefix='.'):
        """ VTK output object.

        :param fields: List of Field or Field, data to be visualized.
        :param identifier: String, unique name/basename out the output files.
        :param prefix: String, directory prefix (where the files go).
        """

        if isinstance(fields, ScalarField):
            self.__fields = [fields]
        elif type(fields) is list:
            self.__fields = fields
        elif type(fields) is tuple:
            self.__fields = list(fields)
        else:
            raise TypeError("Unsupported data type.")

        for field in self.__fields:
            if not isinstance(field.partition.mesh, RectilinearMesh):
                raise TypeError("Currently only fields associated with a rectilinear mesh are supported: %s !" % field.name)

        self.__identifier = identifier
        self.__prefix = prefix + "/"

        names = [field.name for field in self.__fields]

        if len(set(names)) != len(names):
            raise ValueError("Fields need to have a unique identifier!")

        create_dirs(self.__prefix, self.__fields)

        self.__writer = []
        self.__mdwriter = []

        for field in self.__fields:

            data_dtype = None

            for domain in field.partition.domains.itervalues():
                data_dtype = field.d[domain.coordinate].dtype
                self.__writer.append(VTRWriter(generate_dirname(self.__prefix, domain.coordinate)+self.__identifier,
                                               domain.mesh, field.d[domain.coordinate], var_name=field.name,
                                               var_type=field.rank, compressed=False))

            if context.master:
                self.__mdwriter.append(PVTRWriter(self.__prefix+self.__identifier, field.partition.mesh, data_dtype,
                                                  field.partition.meta_data, var_name=field.name, var_type=field.rank,
                                                  stencil=field.partition.stencil))

    def write(self, cycle=None, time=None):
        """ Routine to invoke the datafile genration.

        :param cycle: mesh boundary ((x1,y1,z1),(x2,y2,z2))
        :param time: type of coordinate system
        """

        for writer in self.__writer:
            writer.write(cycle, time)

        for writer in self.__mdwriter:
            writer.write(cycle, time)
