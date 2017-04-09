# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.IValidationRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for schema validation rules.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IValidationRule(object):

    def validate(self, path, schema, value, results):
        raise NotImplementedError('Method from interface definition')