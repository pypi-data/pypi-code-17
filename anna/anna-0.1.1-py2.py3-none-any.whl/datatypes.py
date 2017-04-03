# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

import numpy

_float = numpy.float64
_int = numpy.int64

representations = {
    'number': _float,
    'integer': _int,
    'vector': numpy.array,
}

number = representations['number']
integer = representations['integer']
vector = representations['vector']


def convert_to(representation):
    def converter(item):
        if isinstance(representation, six.text_type):
            return representations[representation](item)
        else:
            return representation(item)
    return converter
