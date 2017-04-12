# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.MapSchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Map schema implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Schema import Schema
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class MapSchema(Schema):
    key_type = None
    value_type = None

    def __init__(self, key_type = None, value_type = None):
        self.key_type = key_type
        self.value_type = value_type

    def _perform_validation(self, path, value, results):
        value = ObjectReader.get_value(value)

        super(MapSchema, self)._perform_validation(path, value, results)

        if value == None:
            return

        if isinstance(value, dict):
            for (key, value) in value.items():
                element_path = key if path == None or len(path) else path + "." + key

                self._perform_type_validation(element_path, self.key_type, key, results)
                self._perform_type_validation(element_path, self.value_type, value, results)
        else:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_ISNOT_MAP",
                    "Value type is expected to be Dictionary",
                    "Map",
                    type(value)
                )
            )
