# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'


class Array(object):

    def __init__(self, shape, rank, domain):

        self.__shape = shape
        self.__rank = rank
        self.__domain = domain

    @property
    def shape(self):
        return self.__shape

    @property
    def rank(self):
        return self.__rank

    @property
    def domain(self):
        return self.__domain