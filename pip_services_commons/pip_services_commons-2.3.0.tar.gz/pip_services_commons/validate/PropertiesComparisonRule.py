# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.PropertiesComparisonRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Properties comparison rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from .ObjectComparator import ObjectComparator
from ..reflect.ObjectReader import ObjectReader

class PropertiesComparisonRule(IValidationRule):
    _property1 = None
    _property2 = None
    _operation = None

    def __init__(self, property1, operation, property2):
        self._property1 = property1
        self._operation = operation
        self._property2 = property2

    def validate(self, path, schema, value, results):
        value1 = ObjectReader.get_property(value, self._property1)
        value2 = ObjectReader.get_property(value, self._property2)

        if not ObjectComparator.compare(value1, self._operation, value2):
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "PROPERTIES_NOT_MATCH",
                    "Property " + str(self._property1) + " is expected to " + str(self._operation) + " property " + str(self._property2),
                    value2,
                    value1
                )
            )
