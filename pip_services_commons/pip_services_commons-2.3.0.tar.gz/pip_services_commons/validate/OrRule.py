# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.OrRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Or rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule

class OrRule(IValidationRule):
    _rules = None

    def __init__(self, *rules):
        self._rules = rules

    def validate(self, path, schema, value, results):
        if self._rules == None or len(self._rules) == 0:
            return

        local_results = []

        for rule in self._rules:
            results_count = len(local_results)
            rule.validate(path, schema, value, local_results)
            if results_count == len(local_results):
                return

        for result in local_results:
            results.append(result)
