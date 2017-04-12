# -*- coding: utf-8 -*-
"""
    pip_services_common.validate.ValidationException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..errors.BadRequestException import BadRequestException

class ValidationException(BadRequestException):

    def __init__(self, correlation_id, results):
        message = ValidationException.compose_message(results)
        super(BadRequestException, self).__init__(correlation_id, 'INVALID_DATA', message)

    @staticmethod
    def compose_message(results):
        message = ''
        message += 'Validation failed'

        if results != None and len(results) > 0:
            first = True
            for result in results:
                if result.type != ValidationResultType.Information:
                    if not first: 
                        message += ': '
                    else:
                        message += ', '
                    message += result.message
                    first = False

        return message

    @staticmethod
    def throw_exception_if_needed(correlation_id, results, strict):
        has_errors = False
        for result in results:
            if result.type == ValidationResultType.Error:
                has_errors = True
            if strict and result.type == ValidationResultType.Warning:
                has_errors = True

        if has_errors:
            raise ValidationException(correlation_id, results)
