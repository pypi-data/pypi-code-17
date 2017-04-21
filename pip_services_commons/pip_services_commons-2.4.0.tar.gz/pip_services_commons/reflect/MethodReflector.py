# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.MethodReflector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Method reflector implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class MethodReflector:

    @staticmethod
    def _is_method(method, name):
        if method == None:
            return False
        if not callable(method):
            return False

        if name.startswith("_"):
            return False

        return True 


    @staticmethod
    def has_method(obj, name):
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Method name cannot be null")

        name = name.lower();

        for method_name in dir(obj): 
            if method_name.lower() != name:
                continue

            method = getattr(obj, method_name)

            if MethodReflector._is_method(method, method_name):
                return True
        
        return False


    @staticmethod
    def invoke_method(obj, name, *args):
        if obj == None:
            raise Exception("Object cannot be null")
        if name == None:
            raise Exception("Method name cannot be null")
        
        name = name.lower()
        
        try:
            for method_name in dir(obj): 
                if method_name.lower() != name:
                    continue

                method = getattr(obj, method_name)

                if MethodReflector._is_method(method, method_name):
                    return method(*args)
        except:
            pass
        
        return None


    @staticmethod
    def get_method_names(obj):
        method_names = []
        
        for method_name in dir(obj):

            method = getattr(obj, method_name)

            if MethodReflector._is_method(method, method_name):
                method_names.append(method_name)

        return method_names
