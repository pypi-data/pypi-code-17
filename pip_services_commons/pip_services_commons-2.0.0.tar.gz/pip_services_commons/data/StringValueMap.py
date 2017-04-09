# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.StringValueMap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    StringValueMap implementation
    
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
from ..reflect.RecursiveObjectReader import RecursiveObjectReader

class StringValueMap(dict):

    def __init__(self, map = None):
        if isinstance(map, dict):
            for (k, v) in map.items():
                self.put(k, v)

    def get_key_names(self):
        names = []
        for (k, _) in self.items():
            names.append(k)
        return names

    def get(self, key):
        key = key.lower()
        for (k, v) in self.items():
            if key == k.lower():
                return v
        return None

    def put(self, key, value):
        self[key] = StringConverter.to_nullable_string(value)

    def remove(self, key):
        self.pop(key)

    def get_as_object(self, key = None):
        if key == None:
            return self.get_as_map()
        else:
            return self.get(key)

    def set_as_object(self, *args):
        if len(args) == 1:
            self.set_as_map(args[0])
        elif len(args) == 2:
            self.put(args[0], args[1])

    def get_as_map(self, key):
        if key == None:
            map = {}
            for (k, v) in self.items():
                map[k] = v
            return map
        else:
            value = self.get(key)
            return MapConverter.to_map(value)

    def set_as_map(self, values):
        self.clear()
        for (k, v) in map.items():
            self.put(k, v)

    def get_as_nullable_string(self, key):
        value = self.get(key)
        return StringConverter.to_nullable_string(value)

    def get_as_string(self, key):
        value = self.get(key)
        return StringConverter.to_string(value)

    def get_as_string_with_default(self, key, default_value):
        value = self.get(key)
        return StringConverter.to_string_with_default(value, default_value)

    def get_as_nullable_boolean(self, key):
        value = self.get(key)
        return BooleanConverter.to_nullable_boolean(value)

    def get_as_boolean(self, key):
        value = self.get(key)
        return BooleanConverter.to_boolean(value)

    def get_as_boolean_with_default(self, key, default_value):
        value = self.get(key)
        return BooleanConverter.to_boolean_with_default(value, default_value)

    def get_as_nullable_integer(self, key):
        value = self.get(key)
        return IntegerConverter.to_nullable_integer(value)

    def get_as_integer(self, key):
        value = self.get(key)
        return IntegerConverter.to_integer(value)

    def get_as_integer_with_default(self, key, default_value):
        value = self.get(key)
        return IntegerConverter.to_integer_with_default(value, default_value)

    def get_as_nullable_long(self, key):
        value = self.get(key)
        return LongConverter.to_nullable_long(value)

    def get_as_long(self, key):
        value = self.get(key)
        return LongConverter.to_long(value)

    def get_as_long_with_default(self, key, default_value):
        value = self.get(key)
        return LongConverter.to_long_with_default(value, default_value)

    def get_as_nullable_float(self, key):
        value = self.get(key)
        return FloatConverter.to_nullable_float(value)

    def get_as_float(self, key):
        value = self.get(key)
        return FloatConverter.to_float(value)

    def get_as_float_with_default(self, key, default_value):
        value = self.get(key)
        return FloatConverter.to_float_with_default(value, default_value)

    def get_as_nullable_datetime(self, key):
        value = self.get(key)
        return DateTimeConverter.to_nullable_datetime(value)

    def get_as_datetime(self, key):
        value = self.get(key)
        return DateTimeConverter.to_datetime(value)

    def get_as_datetime_with_default(self, key, default_value):
        value = self.get(key)
        return DateTimeConverter.to_datetime_with_default(value, default_value)

    def get_as_nullable_type(self, key, value_type):
        value = self.get(key)
        return TypeConverter.to_nullable_type(value_type, value)

    def get_as_type(self, key, value_type):
        value = self.get(key)
        return TypeConverter.to_type(value_type, value)

    def get_as_type_with_default(self, key, value_type, default_value):
        value = self.get(key)
        return TypeConverter.to_type_with_default(value_type, value, default_value)

    # def get_as_array(self, key):
    #     value = self.get(key)
    #     return ArrayConverter.from_value(value)

    def get_as_map(self, key):
        value = self.get(key)
        return MapConverter.from_value(value)


    def clone(self):
        map = StringValueMap()
        map.set_as_map(self)
        return map

    def __str__(self):
        result = ''

        for (k, v) in self.items():
            if len(result) > 0:
                result += ';'

            if v != None:
                result += k + '=' + StringConverter.get_as_string_with_default(v, '')
            else:
                retsult += k

        return result

    @staticmethod
    def from_value(value):
        map = RecursiveObjectReader.get_properties(value)
        return StringValueMap(map)

    @staticmethod
    def from_tuples(*tuples):
        return StringValueMap.from_tuples_array(*tuples)

    @staticmethod
    def from_tuples_array(tuples):
        result = StringValueMap()

        if tuples == None or len(tuples) == 0:
            return result

        index = 0
        while index < len(tuples):
            if index + 1 >= len(tuples):
                break

            key = StringConverter.to_string(tuples[index])
            value = tuples[index + 1]
            index += 2

            result.put(key, value)

        return result

    @staticmethod
    def from_string(line):
        result = StringValueMap()
        
        if line == None or len(line) == 0:
            return result

        tokens = str(line).split(';')
        for token in tokens:
            if len(token) == 0:
                continue
            index = token.find('=')
            key = token[0:index] if index >= 0 else token
            value = token[index + 1:] if index >= 0 else None
            result.put(key, value)

        return result


    @staticmethod
    def from_maps(*maps):
        result = StringValueMap()
        
        if maps == None or len(maps) == 0:
            return result

        for map in maps:
            for (k, v) in map.items():
                key = StringConverter.to_string(k)
                result.put(key, v)

        return result
        