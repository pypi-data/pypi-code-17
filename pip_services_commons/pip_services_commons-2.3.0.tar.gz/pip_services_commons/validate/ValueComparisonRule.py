# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.ValueComparisonRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Value comparison rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ObjectComparator import ObjectComparator
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult

class ValueComparisonRule(IValidationRule):
    _operation = None
    _value = None

    def __init__(self, operation, value):
        self._operation = operation
        self._value = value

    def validate(self, path, schema, value, results):
        if not ObjectComparator.compare(value, self._operation, self._value):
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "BAD_VALUE",
                    str(value) + " is expected to " + str(self._operation) + " " + str(self._value),
                    str(self._operation) + " " + str(self._value),
                    value
                )
            )

