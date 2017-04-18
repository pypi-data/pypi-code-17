# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.MapConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Map conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class MapConverter(object):

    @staticmethod
    def to_nullable_map(value):
        if isinstance(value, dict):
            return value
        elif hasattr(value, "_ast"):
            return value._ast()
        elif hasattr(value, "__iter__"):
            data = {}
            index = 0
            for v in value:
                data[str(index)] = v
                index += 1
            return data
        elif hasattr(value, "__dict__"):
            data = {} 
            for k in dir(value):
                v = getattr(value, k) 
                if not callable(v) and not k.startswith('_'):
                    data[k] = v
            return data
        else:
            return None

        return MapConverter._value_to_map(value)

    @staticmethod
    def to_map(value):
        result = MapConverter.to_nullable_map(value)
        return result if result != None else {}

    @staticmethod
    def to_map_with_default(value, default_value):
        result = MapConverter.to_nullable_map(value)
        return result if result != None else default_value
