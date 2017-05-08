# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'



class DummyStream(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def write(self, text):
        pass

    def flush(self):
        pass