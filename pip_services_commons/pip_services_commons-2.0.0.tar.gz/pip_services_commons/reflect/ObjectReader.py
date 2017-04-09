# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.ObjectReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Object reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.IntegerConverter import IntegerConverter
from .PropertyReflector import PropertyReflector

class ObjectReader:

    @staticmethod
    def get_value(obj):
        # Todo: just a blank implementation for compatibility
        return obj


    @staticmethod
    def has_property(obj, name):
        if obj == None or name == None:
            return False

        name = name.lower()

        if isinstance(obj, dict):
            for (key, value) in obj.items():
                if name == str(key).lower():
                    return True
            return False
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            index = IntegerConverter.to_nullable_integer(name)
            return index != None and index >= 0 and index < len(obj)
        else:
            return PropertyReflector.has_property(obj, name)


    @staticmethod
    def get_property(obj, name):
        if obj == None or name == None:
            return False

        name = name.lower()

        if isinstance(obj, dict):
            for (key, value) in obj.items():
                if name == str(key).lower():
                    return value
            return None
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            index = IntegerConverter.to_nullable_integer(name)
            if index != None and index >= 0 and index < len(obj):
                return obj[index]
            return None
        else:
            return PropertyReflector.get_property(obj, name)


    @staticmethod
    def get_property_names(obj):
        property_names = []

        if isinstance(obj, dict):
            for (key, value) in obj.items():
                property_names.append(key)
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            for index in range(len(obj)):
                property_names.append(str(index))
        else:
            property_names = PropertyReflector.get_property_names(obj)

        return property_names


    @staticmethod
    def get_properties(obj):
        map = {}

        if isinstance(obj, dict):
            for (key, value) in obj.items():
                map[key] = value
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            for index in range(len(obj)):
                map[str(index)] = obj[index]
        else:
            map = PropertyReflector.get_properties(obj)

        return map
