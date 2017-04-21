# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.TypeDescriptor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type descriptor implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..errors.ConfigException import ConfigException

class TypeDescriptor:
    _name = None
    _library = None
        
    def __init__(self, name, library):
        self._name = name
        self._library = library

    def get_name(self):
        return self._name

    def get_library(self):
        return self._library

    def __eq__(self, other):
        if isinstance(other, TypeDescriptor):
            if self._name == None or other._name == None:
                return False
            if self._name != other._name:
                return False
            if self._library == None or other._library == None or self._library == other._library: 
                return True
        
        return False

    def __str__(self):
        result = self._name
        if self._library != None:
            result += ','+ self._library
        return result

    @staticmethod
    def from_string(value):
        if value == None or len(value) == 0:
            return None
                
        tokens = value.split(",")
        if len(tokens) == 1:
            return TypeDescriptor(tokens[0].strip(), None)
        elif len(tokens) == 2:
            return TypeDescriptor(tokens[0].strip(), tokens[1].strip())
        else:
            raise ConfigException(
                None, "BAD_DESCRIPTOR", "Type descriptor " + value + " is in wrong format"
            ).with_details("descriptor", value)

