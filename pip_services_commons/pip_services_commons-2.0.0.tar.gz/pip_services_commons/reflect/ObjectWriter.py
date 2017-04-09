# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.ObjectWriter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Object writer implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.IntegerConverter import IntegerConverter
from .PropertyReflector import PropertyReflector

class ObjectWriter:

    @staticmethod
    def set_property(obj, name, value):
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Property name cannot be null")

        name = name.lower()

        if isinstance(obj, dict):
            for key in obj.keys():
                if name == str(key).lower():
                    obj[key] = value
                    return
            obj[name] = value
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            index = IntegerConverter.to_nullable_integer(name)
            if index == None:
                return
            if index >= 0 and index < len(obj):
                obj[index] = value
            elif isinstance(obj, list):
                while index - 1 >= len(obj):
                    obj.append(None)
                obj.append(value)
        else:
            return PropertyReflector.set_property(obj, name, value)


    @staticmethod
    def set_properties(obj, values):
        if values == None or len(values) == 0:
            return
        
        for (key, value) in values.items():
            ObjectWriter.set_property(obj, key, value)
    