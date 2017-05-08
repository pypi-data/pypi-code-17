# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'


from maui.backend.prototypes.fd import DummyStream
import sys

class Context(object):

    def __init__(self, dtype='float64', master=True):
        
        self.__float_type = dtype
        self.__master = master

    @property
    def dtype(self):
        return self.__float_type

    @property
    def master(self):
        return self.__master

    @property
    def stdout(self):

        if self.master:
            return sys.stdout
        else:
            return DummyStream()

    @property
    def stderr(self):

        if self.master:
            return sys.stderr
        else:
            return DummyStream()
