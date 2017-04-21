# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.AtLeastOneExistRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    At least one exist rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class AtLeastOneExistRule(IValidationRule):
    _properties = None

    def __init__(self, *properties):
        self._properties = properties
    
    def validate(self, path, schema, value, results):
        name = path if path != None else "value"
        found = []

        for prop in self._properties:
            property_value = ObjectReader.get_property(value, prop)
            if property_value != None:
                found.append(prop)

        if len(found) == 0:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_NULL",
                    name + " must have at least one property from " + str(self._properties),
                    self._properties,
                    None
                )
            )
