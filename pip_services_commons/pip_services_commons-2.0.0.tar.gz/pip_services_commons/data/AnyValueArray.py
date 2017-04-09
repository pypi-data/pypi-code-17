# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.AnyValueArray
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    AnyValueArray implementation
    
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


class AnyValueArray(list):

    def __init__(self, values = None):
        if values != None and len(values) > 0:
            for value in values:
                self.append(value)

    def clear(self):
        del self[:]

    def get_as_object(self, index = None):
        if index == None:
            return self.get_as_array()
        else:
            return self[index]

    def set_as_object(self, index = None, value= None):
        if index == None and value != None:
            self.set_as_array(value)
        else:
            self[index] = value

    def get_as_array(self, index):
        if index == None:
            array = []
            for value in self:
                array.append(value)
            return array
        else:
            value = self[index]
            return ArrayConverter.to_array(value)

    def set_as_array(self, values):
        del self[:]
        for value in values:
            self.append(value)

    def get_as_nullable_string(self, index):
        value = self[index]
        return StringConverter.to_nullable_string(value)

    def get_as_string(self, index):
        value = self[index]
        return StringConverter.to_string(value)

    def get_as_string_with_default(self, index, default_value):
        value = self[index]
        return StringConverter.to_string_with_default(value, default_value)

    def get_as_nullable_boolean(self, index):
        value = self[index]
        return BooleanConverter.to_nullable_boolean(value)

    def get_as_boolean(self, index):
        value = self[index]
        return BooleanConverter.to_boolean(value)

    def get_as_boolean_with_default(self, index, default_value):
        value = self[index]
        return BooleanConverter.to_boolean_with_default(value, default_value)

    def get_as_nullable_integer(self, index):
        value = self[index]
        return IntegerConverter.to_nullable_integer(value)

    def get_as_integer(self, index):
        value = self[index]
        return IntegerConverter.to_integer(value)

    def get_as_integer_with_default(self, index, default_value):
        value = self[index]
        return IntegerConverter.to_integer_with_default(value, default_value)

    def get_as_nullable_long(self, index):
        value = self[index]
        return LongConverter.to_nullable_long(value)

    def get_as_long(self, index):
        value = self[index]
        return LongConverter.to_long(value)

    def get_as_long_with_default(self, index, default_value):
        value = self[index]
        return LongConverter.to_long_with_default(value, default_value)

    def get_as_nullable_float(self, index):
        value = self[index]
        return FloatConverter.to_nullable_float(value)

    def get_as_float(self, index):
        value = self[index]
        return FloatConverter.to_float(value)

    def get_as_float_with_default(self, index, default_value):
        value = self[index]
        return FloatConverter.to_float_with_default(value, default_value)

    def get_as_nullable_datetime(self, index):
        value = self[index]
        return DateTimeConverter.to_nullable_datetime(value)

    def get_as_datetime(self, index):
        value = self[index]
        return DateTimeConverter.to_datetime(value)

    def get_as_datetime_with_default(self, index, default_value):
        value = self[index]
        return DateTimeConverter.to_datetime_with_default(value, default_value)

    def get_as_nullable_type(self, index, value_type):
        value = self[index]
        return TypeConverter.to_nullable_type(value_type, value)

    def get_as_type(self, index, value_type):
        value = self[index]
        return TypeConverter.to_type(value_type, value)

    def get_as_type_with_default(self, index, value_type, default_value):
        value = self[index]
        return TypeConverter.to_type_with_default(value_type, value, default_value)

    # def get_as_array(self, index):
    #     value = self[index]
    #     return ArrayConverter.from_value(value)

    def get_as_map(self, index):
        value = self[index]
        return MapConverter.from_value(value)


    def contains(self, value):
        str_value = StringConverter.to_nullable_string(value)

        for element in self:
            str_element = StringConverter.to_string(element)

            if str_value == None and str_element == None:
                return True
            if str_value == None or str_element == None:
                continue
            
            if str_value == str_element:
                return True

        return False


    def contains_as_type(self, value_type, value):
        typed_value = TypeConverter.to_nullable_type(value_type, value)

        for element in self:
            typed_element = TypeConverter.to_type(value_type, element)

            if typed_value == None and typed_element == None:
                return True
            if typed_value == None or typed_element == None:
                continue
            
            if typed_value == typed_element:
                return True

        return False

    def clone(self):
        array = AnyValueArray()
        array.set_as_array(self)
        return array

    def __str__(self):
        result = ''

        for element in self:
            if len(result) > 0:
                result += ','
            result += StringConverter.to_string_with_default(element, '')

        return result

    @staticmethod
    def from_values(*values):
        return AnyValueArray(values)

    @staticmethod
    def from_value(value):
        value = ArrayConverter.to_nullable_array(value)
        if value != None:
            return AnyValueArray(value)
        return AnyValueArray()

    @staticmethod
    def from_string(values, separator, remove_duplicates = False):
        result = AnyValueArray()

        if values == None or len(values) == 0:
            return result

        items = str(values).split(separator)
        for item in items:
            if (item != None and len(item) > 0) or remove_duplicates == False:
                result.append(item)

        return result
    