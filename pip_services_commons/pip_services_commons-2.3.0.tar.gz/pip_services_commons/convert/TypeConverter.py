# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.TypeConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import types
from datetime import datetime

from .StringConverter import StringConverter
from .BooleanConverter import BooleanConverter
from .IntegerConverter import IntegerConverter
from .LongConverter import LongConverter
from .FloatConverter import FloatConverter
from .DateTimeConverter import DateTimeConverter
from .ArrayConverter import ArrayConverter
from .MapConverter import MapConverter
from .TypeCode import TypeCode

class TypeConverter(object):
        
    @staticmethod
    def to_type_code(value):
        if value == None:
            return TypeCode.Unknown

        if not isinstance(value, type):
            value = type(value)

        if value is list:
            return TypeCode.Array
        elif value is tuple:
            return TypeCode.Array
        elif value is set:
            return TypeCode.Array
        elif value is bool:
            return TypeCode.Boolean
        elif value is int:
            return TypeCode.Integer
        elif value is long:
            return TypeCode.Long
        elif value is float:
            return TypeCode.Float
        elif value is str:
            return TypeCode.String
        elif value is unicode:
            return TypeCode.String
        elif value is datetime:
            return TypeCode.DateTime
        elif value is dict:
            return TypeCode.Map
            
        return TypeCode.Object


    @staticmethod
    def to_nullable_type(value_type, value):
        result_type = TypeConverter.to_type_code(value_type)

        if value == None:
            return None
        if isinstance(value, type):
            return value
        
        # Convert to known types
        if result_type == TypeCode.String:
            return StringConverter.to_nullable_string(value)
        elif result_type == TypeCode.Integer:
            return IntegerConverter.to_nullable_integer(value)
        elif result_type == TypeCode.Long:
            return LongConverter.to_nullable_long(value)
        elif result_type == TypeCode.Float:
            return FloatConverter.to_nullable_float(value)
        elif result_type == TypeCode.Double:
            return FloatConverter.to_nullable_float(value)
        elif result_type == TypeCode.Duration:
            return LongConverter.to_nullable_long(value)
        elif result_type == TypeCode.DateTime:
            return DateTimeConverter.to_nullable_datetime(value)
        elif result_type == TypeCode.Array:
            return ArrayConverter.to_nullable_array(value)
        elif result_type == TypeCode.Map:
            return MapConverter.to_nullable_map(value)

        return None


    @staticmethod
    def to_type(value_type, value):
        # Convert to the specified type
        result = TypeConverter.to_nullable_type(value_type, value)
        if result != None:
            return result

        # Define and return default value based on type
        result_type = TypeConverter.to_type_code(value_type)
        if result_type == TypeCode.String:
            return None
        elif result_type == TypeCode.Integer:
            return 0
        elif result_type == TypeCode.Long:
            return 0L
        elif result_type == TypeCode.Float:
            return 0.0
        else:
            return None


    @staticmethod
    def to_type_with_default(value_type, value, default_value):
        result = TypeConverter.to_nullable_type(value_type, value)
        return result if result != None else default_value
