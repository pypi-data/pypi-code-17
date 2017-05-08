# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.field import ScalarField
from maui.field import View


class ADE(object):

    def __init__(self, host, fields, bounds, initializer=None):

        self.__bounds = bounds
        self.__initializer = None
        self.__host = View(host, bounds=bounds)

        self.__partition = self.__host.partition.copy(bounds=bounds)

        self.__fields = dict()

        for key in fields.keys():
            self.__fields[key] = ScalarField(self.__partition, key, fields[key], bounds=bounds)

        if initializer is not None and callable(initializer):
            initializer(self.__fields)

    @property
    def host(self):
        return self.__host

    def view(self, field):
        return View(field, partition=self.__partition, bounds=self.__bounds)

    @property
    def fields(self):
        return self.__fields

    def get_state(self):
        return self.__fields

    def set_state(self, state_dict):
        self.__fields = state_dict

