# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.PropertyReflector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Property reflector implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class PropertyReflector:

    @staticmethod
    def _is_property(property, name):
        if callable(property):
            return False

        if name.startswith("_"):
            return False

        return True 


    @staticmethod
    def has_property(obj, name):
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Property name cannot be null")

        name = name.lower();

        for property_name in dir(obj): 
            if property_name.lower() != name:
                continue

            property = getattr(obj, property_name)

            if PropertyReflector._is_property(property, property_name):
                return True
        
        return False


    @staticmethod
    def get_property(obj, name):
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Property name cannot be null")
        
        name = name.lower()
        
        try:
            for property_name in dir(obj): 
                if property_name.lower() != name:
                    continue

                property = getattr(obj, property_name)

                if PropertyReflector._is_property(property, property_name):
                    return property
        except:
            pass
        
        return None


    @staticmethod
    def get_property_names(obj):
        property_names = []
        
        for property_name in dir(obj):

            property = getattr(obj, property_name)

            if PropertyReflector._is_property(property, property_name):
                property_names.append(property_name)

        return property_names


    @staticmethod
    def get_properties(obj):
        properties = {}
        
        for property_name in dir(obj):

            property = getattr(obj, property_name)

            if PropertyReflector._is_property(property, property_name):
                properties[property_name] = property

        return properties


    @staticmethod
    def set_property(obj, name, value):
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Property name cannot be null")
        
        name = name.lower()
        
        try:
            for property_name in dir(obj): 
                if property_name.lower() != name:
                    continue

                property = getattr(obj, property_name)

                if PropertyReflector._is_property(property, property_name):
                    setattr(obj, property_name, value)
        except:
            pass


    @staticmethod
    def set_properties(obj, values):
        if values == None or len(values) == 0:
            return

        for (name, value) in values:
            PropertyReflector.set_property(obj, name, value)

