# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np

U64CHAR = np.dtype(np.uint64).char


class Base64EncodedBuffer(object):

    def __init__(self, buffer):

        from struct import pack
        from base64 import b64encode

        self.__header = b64encode(pack(U64CHAR, len(buffer)))
        self.__data = b64encode(buffer)

    def __len__(self):
        return len(self.__header) + len(self.__data)

    @property
    def data(self):
        return self.__data

    @property
    def header(self):
        return self.__header


class Base64ZLibEncodedBuffer(object):

    def __init__(self, buffer):

        from struct import pack
        from base64 import b64encode
        from zlib import compress

        compressed_buffer = compress(buffer)
        compressed_header = [1, len(buffer), len(buffer), len(compressed_buffer)]

        self.__header = b64encode(pack(U64CHAR*len(compressed_header), *compressed_header))
        self.__data = b64encode(compressed_buffer)

    def __len__(self):
        return len(self.__header) + len(self.__data)

    @property
    def data(self):
        return self.__data

    @property
    def header(self):
        return self.__header
