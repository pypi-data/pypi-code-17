# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.Schema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation schema for complex objects.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from .ValidationException import ValidationException
from ..reflect.ObjectReader import ObjectReader
from ..reflect.TypeMatcher import TypeMatcher

class Schema(object):
    required = None
    rules = None

    def __init__(self, required = False, rules = None):
        self.required = required
        self.rules = rules if rules != None else []

    def make_required(self):
        self.required = True
        return self

    def make_optional(self):
        self.required = False
        return self

    def with_rule(self, rule):
        self.rules = self.rules if self.rules != None else []
        self.rules.append(rule)
        return self

    def _perform_validation(self, path, value, results):
        if value == None:
            # Check for required values
            if self.required:
                results.append(
                    ValidationResult(
                        path,
                        ValidationResultType.Error,
                        "VALUE_IS_NULL",
                        "value cannot be null",
                        "NOT NULL",
                        None
                    )
                )
        else:
            value = ObjectReader.get_value(value)

            # Check validation rules
            if self.rules != None:
                for rule in self.rules:
                    rule.validate(path, self, value, results)

    def _perform_type_validation(self, path, typ, value, results):
        # If type it not defined then skip
        if typ == None:
            return

        # Perform validation against schema
        if isinstance(typ, Schema):
            schema = typ
            schema._perform_validation(path, value, results)
            return

        # If value is null then skip
        value = ObjectReader.get_value(value)
        if value == None:
            return

        value_type = type(value)

        # Match types
        if TypeMatcher.match_type(typ, value_type):
            return
        
        # Generate type mismatch error
        results.append(
            ValidationResult(
                path,
                ValidationResultType.Error,
                "TYPE_MISMATCH",
                "Expected type " + str(typ) + " but found " + str(value_type),
                typ,
                value_type
            )
        )

    def validate(self, value):
        results = []
        self._perform_validation("", value, results)
        return results

    def validate_and_throw_exception(self, correlation_id, value, strict = False):
        results = self.validate(value)
        ValidationException.throw_exception_if_needed(correlation_id, results, strict)
