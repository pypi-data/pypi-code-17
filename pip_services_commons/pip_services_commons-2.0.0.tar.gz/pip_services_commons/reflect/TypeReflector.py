# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.TypeReflector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type reflector implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import importlib

from ..errors.NotFoundException import NotFoundException

class TypeReflector:
    
    @staticmethod
    def get_type(name, library):
        if name == None:
            raise Exception("Class name cannot be null")
        if library == None:
            raise Exception("Module name cannot be null")

        try:
            module = importlib.import_module(library)
            return getattr(module, name)
        except:
           return None

    @staticmethod
    def get_type_by_descriptor(descriptor):
        if descriptor == None:
            raise Exception("Type descriptor cannot be null")

        return TypeReflector.get_type(descriptor.get_name(), descriptor.get_library())

    @staticmethod
    def create_instance(name, library, *args):
        obj_type = TypeReflector.get_type(name, library)
        if obj_type == None:
            raise NotFoundException(
                None, "TYPE_NOT_FOUND", "Type " + name + "," + library + " was not found"
            ).with_details("type", name).with_details("library", library)
        
        return obj_type(*args)

    @staticmethod
    def create_instance_by_type(obj_type, *args):
        if obj_type == None:
            raise Exception("Class type cannot be null")

        return obj_type(*args)

    @staticmethod
    def create_instance_by_descriptor(descriptor, *args):
        if descriptor == None:
            raise Exception("Type descriptor cannot be null")

        return TypeReflector.create_instance(descriptor.get_name(), descriptor.get_library())
