# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.ValidationResult
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation result implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ValidationResult(object):
    path = None
    type = None
    code = None
    message = None
    expected = None
    actual = None

    def __init__(self, path = None, type = None, code = None, message = None, expected = None, actual = None):
        self.path = path
        self.type = type
        self.code = code
        self.message = message
        self.expected = expected
        self.actual = actual
