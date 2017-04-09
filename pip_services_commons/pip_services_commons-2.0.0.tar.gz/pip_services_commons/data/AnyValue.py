# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.AnyValue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    AnyValue implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..convert.TypeConverter import TypeConverter
from ..convert.StringConverter import StringConverter
from ..convert.BooleanConverter import BooleanConverter
from ..convert.IntegerConverter import IntegerConverter
from ..convert.LongConverter import LongConverter
from ..convert.FloatConverter import FloatConverter
from ..convert.DateTimeConverter import DateTimeConverter
from ..convert.ArrayConverter import ArrayConverter
from ..convert.MapConverter import MapConverter


class AnyValue(object):
    value = None

    def __init__(self, value = None):
        if isinstance(value, AnyValue):
            self.value = value._value
        else:
            self.value = value

    def get_type_code(self):
        return TypeConverter.to_type_code(self.value)

    def get_as_object(self):
        return self.value

    def set_as_object(self, value):
        self.value = value
    
    def get_as_nullable_string(self):
        return StringConverter.to_nullable_string(self.value)

    def get_as_string(self):
        return StringConverter.to_string(self.value)

    def get_as_string_with_default(self, default_value):
        return StringConverter.to_string_with_default(self.value, default_value)

    def get_as_nullable_boolean(self):
        return BooleanConverter.to_nullable_boolean(self.value)

    def get_as_boolean(self):
        return BooleanConverter.to_boolean(self.value)

    def get_as_boolean_with_default(self, default_value):
        return BooleanConverter.to_boolean_with_default(self.value, default_value)

    def get_as_nullable_integer(self):
        return IntegerConverter.to_nullable_integer(self.value)

    def get_as_integer(self):
        return IntegerConverter.to_integer(self.value)

    def get_as_integer_with_default(self, default_value):
        return IntegerConverter.to_integer_with_default(self.value, default_value)

    def get_as_nullable_long(self):
        return LongConverter.to_nullable_long(self.value)

    def get_as_long(self):
        return LongConverter.to_long(self.value)

    def get_as_long_with_default(self, default_value):
        return LongConverter.to_long_with_default(self.value, default_value)

    def get_as_nullable_float(self):
        return FloatConverter.to_nullable_float(self.value)

    def get_as_float(self):
        return FloatConverter.to_float(self.value)

    def get_as_float_with_default(self, default_value):
        return FloatConverter.to_float_with_default(self.value, default_value)

    def get_as_nullable_datetime(self):
        return DateTimeConverter.to_nullable_datetime(self.value)

    def get_as_datetime(self):
        return DateTimeConverter.to_datetime(self.value)

    def get_as_datetime_with_default(self, default_value):
        return DateTimeConverter.to_datetime_with_default(self.value, default_value)

    def get_as_nullable_type(self, value_type):
        return TypeConverter.to_nullable_type(value_type, self.value)

    def get_as_type(self, value_type):
        return TypeConverter.to_type(value_type, self.value)

    def get_as_type_with_default(self, value_type, default_value):
        return TypeConverter.to_type_with_default(value_type, self.value, default_value)

    def get_as_array(self):
        return ArrayConverter.from_value(self.value)

    def get_as_map(self):
        return MapConverter.from_value(self.value)


    def __eq__(self, other):
        if other == None and self.value == None:
            return True
        if other == None or self.value == None:
            return False

        if isinstance(other, AnyValue):
            other = other._value

        if other == self.value:
            return True
        
        str_value1 = StringConverter.to_string(self.value)
        str_value2 = StringConverter.to_string(other)

        if str_value1 == None or str_value2 == None:
            return False

        return str_value1 == str_value2


    def __ne__(self, other):
        return not self.__eq__(other)


    def equals_as(self, value_type, other):
        if other == None and self.value == None:
            return True
        if other == None or self.value == None:
            return False

        if isinstance(other, AnyValue):
            other = other._value

        if other == self.value:
            return True
        
        value1 = TypeConverter.to_type(value_type, self.value)
        value2 = TypeConverter.to_type(value_type, other)

        if value1 == None or value2 == None:
            return False

        return value1 == value2

    def __str__(self):
        return StringConverter(self.value)