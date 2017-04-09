# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.PropertySchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation schema for object properties
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Schema import Schema

class PropertySchema(Schema):
    name = None
    value_type = None 

    def __init__(self, name = None, value_type = None):
        self.name = name
        self.value_type = value_type

    def _perform_validation(self, path, value, results):
        path = self.name if path == None or len(path) == 0 else path + "." + self.name

        super(PropertySchema, self)._perform_validation(path, value, results)
        self._perform_type_validation(path, self.value_type, value, results)
