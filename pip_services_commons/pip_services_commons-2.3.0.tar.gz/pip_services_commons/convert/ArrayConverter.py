# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.ArrayConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Array conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ArrayConverter(object):

    @staticmethod
    def to_nullable_array(value):
        # Shortcuts
        if value == None:
            return None
        if type(value) == list:
            return value 

        if type(value) in [tuple, set]:
            return list(value)
            
        return [value]

    @staticmethod
    def to_array(value):
        return ArrayConverter.to_array_with_default(value, [])

    @staticmethod
    def to_array_with_default(value, default_value):
        result = ArrayConverter.to_nullable_array(value)
        return result if result != None else default_value

    @staticmethod
    def list_to_array(value):
        if value == None:
            return []
        elif type(value) in [list, tuple, set]:
            return list(value)
        elif type(value) in [str, unicode]:
            return value.split(',')
        else:
            return [value]
