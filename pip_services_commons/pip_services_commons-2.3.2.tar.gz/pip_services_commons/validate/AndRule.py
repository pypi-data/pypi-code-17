# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.AndRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    And rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule

class AndRule(IValidationRule):
    _rules = None

    def __init__(self, *rules):
        self._rules = rules
    
    def validate(self, path, schema, value, results):
        if _rules == None:
            return

        for rule in self._rules:
            rule.validate(path, schema, value, results)
