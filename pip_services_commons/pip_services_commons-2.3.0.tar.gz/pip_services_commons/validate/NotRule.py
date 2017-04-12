# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.NotRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Not rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResult import ValidationResult
from .ValidationResultType import ValidationResultType

class NotRule(IValidationRule):
    _rule = None

    def __init__(self, rule):
        self._rule = rule
    
    def validate(self, path, schema, value, results):
        if self._rule == None:
            return

        local_results = []

        self._rule.validate(path, schema, value, local_results)

        if len(local_results) > 0:
            return

        results.append(ValidationResult(
            path,
            ValidationResultType.Error,
            'NOT_FAILED',
            'Negative check failed',
            None,
            None
        ))
