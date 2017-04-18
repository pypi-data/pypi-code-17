# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.TypeMatcher
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type matcher implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

class TypeMatcher:

    @staticmethod
    def match_value(expected_type, actual_value):
        if expected_type == None:
            return True
        if actual_value == None:
            raise Exception("Actual value cannot be null")

        return TypeMatcher.match_type(expected_type, type(actual_value))


    @staticmethod
    def match_type(expected_type, actual_type):
        if expected_type == None:
            return True
        if actual_type == None:
            raise Exception("Actual type cannot be null")

        if isinstance(expected_type, type):
            return issubclass(actual_type, expected_type)
        
        if isinstance(expected_type, str):
            return TypeMatcher.match_type_by_name(expected_type, actual_type)

        return False


    @staticmethod
    def match_value_by_name(expected_type, actual_value):
        if expected_type == None:
            return True
        if actual_value == None:
            raise Exception("Actual value cannot be null")

        return TypeMatcher.match_type_by_name(expected_type, type(actual_value))


    @staticmethod
    def match_type_by_name(expected_type, actual_type):
        if expected_type == None:
            return True
        if actual_type == None:
            raise Exception("Actual type cannot be null")
        
        expected_type = expected_type.lower()

        if actual_type.__name__.lower() == expected_type: 
            return True
        elif expected_type == "object":
            return True
        elif expected_type == "int" or expected_type == "integer":
            return issubclass(actual_type, int) or issubclass(actual_type, long)
        elif expected_type == "long":
            return issubclass(actual_type, long)
        elif expected_type == "float" or expected_type == "double":
            return issubclass(actual_type, float)
        elif expected_type == "string":
            return issubclass(actual_type, str) or issubclass(actual_type, unicode)
        elif expected_type == "bool" or expected_type == "boolean":
            return issubclass(actual_type, bool)
        elif expected_type == "date" or expected_type == "datetime":
            return issubclass(actual_type, datetime.datetime) or issubclass(actual_type. datetime.date)
        elif expected_type == "timespan" or expected_type == "duration":
            return issubclass(actual_type, int) or issubclass(actual_type, long) or issubclass(actual_type, float)
        elif expected_type == "enum":
            return issubclass(actual_type, str) or issubclass(actual_type, int)
        elif expected_type == "map" or expected_type == "dict" or expected_type == "dictionary":
            return issubclass(actual_type, dict)
        elif expected_type == "array" or expected_type == "list":
            return issubclass(actual_type, list) or issubclass(actual_type, tuple) or issubclass(actual_type, set)
        elif expected_type.endswith("[]"):
            # Todo: Check subtype
            return issubclass(actual_type, list) or issubclass(actual_type, tuple) or issubclass(actual_type, set)
        else:
            return False
