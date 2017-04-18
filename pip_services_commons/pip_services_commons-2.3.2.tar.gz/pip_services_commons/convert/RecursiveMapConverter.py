# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.RecursiveMapConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Recursive map conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class RecursiveMapConverter(object):

    @staticmethod
    def _value_to_map(value, classkey = None):
        if isinstance(value, dict):
            data = {}
            for (k, v) in value.items():
                data[k] = RecursiveMapConverter._value_to_map(v, classkey)
            return data
        elif hasattr(value, "_ast"):
            return RecursiveMapConverter._value_to_map(value._ast())
        elif hasattr(value, "__iter__"):
            return [RecursiveMapConverter._value_to_map(v, classkey) for v in value]
        elif hasattr(value, "__dict__"):
            data = {} 
            for k in dir(value):
                v = getattr(value, k)
                if not callable(v) and not k.startswith('_'):
                    data[k] = RecursiveMapConverter._value_to_map(v, classkey)
            if classkey is not None and hasattr(value, "__class__"):
                data[classkey] = value.__class__.__name__
            return data
        else:
            return value

    @staticmethod
    def to_nullable_map(value):
        if value == None:
            return None

        return RecursiveMapConverter._value_to_map(value)

    @staticmethod
    def to_map(value):
        result = RecursiveMapConverter.to_nullable_map(value)
        return result if result != None else {}

    @staticmethod
    def to_map_with_default(value, default_value):
        result = RecursiveMapConverter.to_nullable_map(value)
        return result if result != None else default_value
