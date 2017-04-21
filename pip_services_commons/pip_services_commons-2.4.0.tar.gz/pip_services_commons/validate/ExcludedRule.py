# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.ExcludedRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Excluded rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class ExcludedRule(IValidationRule):
    _values = None

    def __init__(self, *values):
        self._values = values

    def validate(self, path, schema, value, results):
        name = path if path != None else "value"
        found = False

        for this_value in self._values:
            if this_value != None and this_value == value:
                found = True
                break

        if found:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_INCLUDED",
                    name + " must not be one of " + str(self._values),
                    self._values,
                    value
                )
            )
