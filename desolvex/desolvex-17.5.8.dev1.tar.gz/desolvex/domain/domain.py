# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.field import ScalarField
from maui.mesh import CartesianMesh
from copy import deepcopy


class Domain(object):

    def __init__(self, meshes, fields, variables, coordinates=('x', 'y', 'z'), initializer=None):

        self.__variables = variables

        # Every domain has the property 'iteration' which is an identifier for the state
        if 'iteration' not in variables.keys():
            self.__variables['iteration'] = 0

        # setup fields
        self.__fields = dict()

        for key in fields.keys():
            if type(fields[key]) is dict:
                for name in fields[key].keys():
                    if name in coordinates:
                        coordinate = name
                        for name in fields[key][coordinate].keys():
                            self.__fields[name] = ScalarField(meshes[key][coordinate], name, fields[key][coordinate][name])
                    else:
                        self.__fields[name] = ScalarField(meshes[key], name, fields[key][name])

        # initialize fields using initializer function
        if initializer is not None and callable(initializer):
            initializer(self.__fields)

        self.__ades = dict()

    def get_state(self):

        state = dict()
        for key in self.__fields.keys():
            for key2 in self.__fields[key].d.keys():
                state[key+'_'+str(key2)] = self.__fields[key].d[key2].copy()

        for key in self.__variables.keys():
            state['var_'+key] = deepcopy(self.__variables[key])

        for key in self.__ades.keys():
            for key2 in self.__ades[key].get_state().keys():
                for key3 in self.__ades[key].get_state()[key2].d.keys():
                    state['ade_'+key+'_'+key2+'_'+str(key3)] = self.__ades[key].get_state()[key2].d[key3].copy()

        return state

    def set_state(self, state_dict):

        for key in self.__fields.keys():
            for key2 in self.__fields[key].d.keys():
                self.__fields[key].d[key2][:] = state_dict[key+'_'+str(key2)][:]

        for key in self.__variables.keys():
            self.__variables[key] = deepcopy(state_dict['var_'+key])

        # TODO: pml korrekt zurueckspielen!!!
        for key in self.__ades.keys():

            for key2 in self.__ades[key].get_state().keys():
                for key3 in self.__ades[key].get_state()[key2].d.keys():
                    self.__ades[key].get_state()[key2].d[key3][:] = state_dict['ade_'+key+'_'+key2+'_'+str(key3)][:]

    def add_ade(self, name, ade):
        if not name in self.__ades.keys():
            self.__ades[name] = ade

        for key in ade.get_state().keys():
            self.__fields['ade_'+name+'_'+key] = ade.get_state()[key]

    @property
    def fields(self):
        return self.__fields

    @property
    def variables(self):
        return self.__variables
