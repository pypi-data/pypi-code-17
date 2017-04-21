# -*- coding: utf-8 -*-
"""
    pip_services_commons.reflect.RecursiveObjectWriter.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Recursive object writer implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ObjectReader import ObjectReader
from .ObjectWriter import ObjectWriter
from .RecursiveObjectReader import RecursiveObjectReader

class RecursiveObjectWriter:

    @staticmethod
    def _create_property(obj, name):
        return {}


    @staticmethod
    def _perform_set_property(obj, names, name_index, value):
        if name_index < len(names) - 1:
            sub_obj = ObjectReader.get_property(obj, names[name_index])
            if sub_obj != None:
                RecursiveObjectWriter._perform_set_property(sub_obj, names, name_index + 1, value)
            else:
                sub_obj = RecursiveObjectWriter._create_property(obj, names[name_index])
                if sub_obj != None:
                    RecursiveObjectWriter._perform_set_property(sub_obj, names, name_index + 1, value)
                    ObjectWriter.set_property(obj, names[name_index], sub_obj)
        else:
            ObjectWriter.set_property(obj, names[name_index], value)


    @staticmethod
    def set_property(obj, name, value):
        if obj == None or name == None:
            return

        names = name.split(".")
        if names == None or len(names) == 0:
            return

        RecursiveObjectWriter._perform_set_property(obj, names, 0, value)


    @staticmethod
    def set_properties(obj, values):
        if values == None or len(values) == 0:
            return
        
        for (key, value) in values.items():
            RecursiveObjectWriter.set_property(obj, key, value)


    @staticmethod
    def copy_properties(dest, src):
        if dest == None or src == None:
            return
        
        values = RecursiveObjectReader.get_properties(src)
        RecursiveObjectWriter.set_properties(dest, values)
