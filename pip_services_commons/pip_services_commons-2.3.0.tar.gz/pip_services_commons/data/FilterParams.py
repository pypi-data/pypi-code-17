# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.FilterParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Free-form filter parameters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .StringValueMap import StringValueMap

class FilterParams(StringValueMap):
    """
    Stores free-form parameters as key-value pairs
    """

    def __init__(self, map = None):
        if map != None:
            for (key, value) in map.items():
                self[key] = value

    @staticmethod
    def from_value(value):
        return FilterParams(value)

    @staticmethod
    def from_tuples(*tuples):
        map = StringValueMap.from_tuples_array(tuples)
        return FilterParams(map)

    @staticmethod
    def from_string(line):
        map = StringValueMap.from_string(line)
        return FilterParams(map)
