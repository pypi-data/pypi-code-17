# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.Parameters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Parameters component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..data.AnyValueMap import AnyValueMap
from ..convert.JsonConverter import JsonConverter
from ..reflect.RecursiveObjectReader import RecursiveObjectReader
from ..reflect.RecursiveObjectWriter import RecursiveObjectWriter
from ..reflect.ObjectWriter import ObjectWriter

class Parameters(AnyValueMap):

    def __init__(self, map = None):
        super(Parameters, self).__init__(map)

    def get(self, key):
        if key == None or key == '':
            return None
        elif key.find('.') > 0:
            return RecursiveObjectReader.get_property(self, key)
        else:
            return super(Parameters, self).get(key)

    def put(self, key, value):
        if key == None or key == '':
            return None
        elif key.find('.') > 0:
            RecursiveObjectWriter.set_property(self, key, value)
            return value
        else:
            self[key] = value
            return value

    def get_as_nullable_parameters(self, key):
        value = self.get_as_nullable_map(key)
        return Parameters(value) if value != None else None

    def get_as_parameters(self, key):
        value = self.get_as_map(key)
        return Parameters(value)

    def get_as_parameters_with_default(self, key, default_value):
        result = get_as_nullable_parameters(key)
        return result if result != None else default_value

    def contains_key(self, key):
        return RecursiveObjectReader.has_property(self, key)

    def override(self, parameters, recursive = False):
        result = Parameters()

        if recursive:
            RecursiveObjectWriter.copy_properties(result, self)
            RecursiveObjectWriter.copy_properties(result, parameters)
        else:
            ObjectWriter.set_properties(result, self)
            ObjectWriter.set_properties(result, parameters)

        return result

    def set_defaults(self, default_values, recursive = False):
        result = Parameters()

        if recursive:
            RecursiveObjectWriter.copy_properties(result, default_values)
            RecursiveObjectWriter.copy_properties(result, self)
        else:
            ObjectWriter.set_properties(result, default_values)
            ObjectWriter.set_properties(result, self)

        return result

    def assign_to(self, value):
        if value == None or len(self) == 0:
            return

        ObjectWriter.copy_properties(value, self)
        
    def pick(self, *props):
        result = Parameters()
        for prop in props:
            if self.contains_key(prop):
                result.put(prop, self.get(prop))
        return result

    def omit(self, *props):
        result = Parameters(self)
        for prop in props:
            del result[prop]
        return result

    def to_json(self):
        return JsonConverter.to_json(self)

    @staticmethod
    def from_value(value):
        map = value if isinstance(value, dict) else RecursiveObjectReader.get_properties(value)
        return Parameters(map)

    @staticmethod
    def from_tuples(*tuples):
        map = AnyValueMap.from_tuples_array(tuples)
        return Parameters(map)

    @staticmethod
    def merge_params(*parameters):
        map = AnyValueMap.from_maps(parameters)
        return Parameters(map)

    @staticmethod
    def from_json(json):
        map = JsonConverter.to_nullable_map(json)
        return Parameters(map)

    @staticmethod
    def from_config(config):
        result = Parameters()
        
        if config == None or len(config) == 0:
            return result
        
        for (key, value) in config.items():
            result.put(key, value)
        
        return result
