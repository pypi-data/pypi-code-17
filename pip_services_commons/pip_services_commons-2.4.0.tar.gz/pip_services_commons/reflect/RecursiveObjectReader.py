# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.RecursiveObjectReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Recursive object reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.TypeCode import TypeCode
from ..convert.TypeConverter import TypeConverter
from .ObjectReader import ObjectReader

class RecursiveObjectReader:

    @staticmethod
    def _perform_has_property(obj, names, name_index):
        if name_index < len(names) - 1:
            value  = ObjectReader.get_property(obj, names[name_index])
            if value != None:
                return RecursiveObjectReader._perform_has_property(value, names, name_index + 1)
            else:
                return False
        else:
            return ObjectReader.has_property(obj, names[name_index])


    @staticmethod
    def has_property(obj, name):
        if obj == None or name == None:
            return False

        names = name.split(".")
        if names == None or len(names) == 0: 
            return False

        return RecursiveObjectReader._perform_has_property(obj, names, 0)

    
    @staticmethod
    def _perform_get_property(obj, names, name_index):
        if name_index < len(names) - 1:
            value = ObjectReader.get_property(obj, names[name_index])
            if value != None:
                return RecursiveObjectReader._perform_get_property(value, names, name_index + 1)
            else:
                return None
        else:
            return ObjectReader.get_property(obj, names[name_index])


    @staticmethod
    def get_property(obj, name):
        if obj == None or name == None:
            return None

        names = name.split(".")
        if names == None or len(names) == 0:
            return None

        return RecursiveObjectReader._perform_get_property(obj, names, 0)


    @staticmethod
    def _is_simple_value(value):
        code = TypeConverter.to_type_code(value)
        return code != TypeCode.Array and code != TypeCode.Map and code != TypeCode.Object


    @staticmethod
    def _perform_get_property_names(obj, path, result, cycle_detect):
        map = ObjectReader.get_properties(obj)
        
        if len(map) != 0 and len(cycle_detect) < 100:
            cycle_detect.append(obj)
            try:
                for (key, value) in map.items():
                    # Prevent cycles 
                    if value in cycle_detect:
                        continue

                    key = path + "." + key if path != None else key
                    
                    # Add simple values directly
                    if RecursiveObjectReader._is_simple_value(value):
                        result.append(key)
                    # Recursively go to elements
                    else:
                        RecursiveObjectReader._perform_get_property_names(value, key, result, cycle_detect)
            finally:
                cycle_detect.remove(obj)
        else:
            if path != None:
                result.append(path)


    @staticmethod
    def get_property_names(obj):
        property_names = []
        
        if obj != None:
            cycle_detect = []
            RecursiveObjectReader._perform_get_property_names(obj, None, property_names, cycle_detect)

        return property_names

    @staticmethod
    def _perform_get_properties(obj, path, result, cycle_detect):
        map = ObjectReader.get_properties(obj)
        
        if len(map) != 0 and len(cycle_detect) < 100:
            cycle_detect.append(obj)
            try:
                for (key, value) in map.items():
                    # Prevent cycles 
                    if value in cycle_detect:
                        continue

                    key = path + "." + key if path != None else key
                    
                    # Add simple values directly
                    if RecursiveObjectReader._is_simple_value(value):
                        result[key] = value
                    # Recursively go to elements
                    else:
                        RecursiveObjectReader._perform_get_properties(value, key, result, cycle_detect)
            finally:
                cycle_detect.remove(obj)
        else:
            if path != None:
                result[path] = obj


    @staticmethod
    def get_properties(obj):
        properties = {}
        
        if obj != None:
            cycle_detect = []
            RecursiveObjectReader._perform_get_properties(obj, None, properties, cycle_detect)

        return properties
