# -*- coding: utf-8 -*-
"""
    pip_services_commons.errors.ApplicationException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Application exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import traceback

from .ErrorCategory import ErrorCategory

class ApplicationException(Exception):
    """
    Base class for all errors thrown by microservice implementation
    """

    message = None
    category = ErrorCategory.Unknown
    status = 500
    code = 'UNKNOWN'
    details = None
    correlation_id = None
    stack_trace = None
    cause = None
    
    def __init__(self, category = ErrorCategory.Unknown, correlation_id = None, code = 'UNKNOWN', message = 'Unknown error'):
        super(ApplicationException, self).__init__(message)
        
        self.message = message
        self.correlation_id = correlation_id;
        self.code = code
        self.category = category
        self.name = code
        self.stack_trace = traceback.format_exc()
        
    def __str__(self):
        return str(self.message) if self.message != None else 'Unknown error'

    def to_json(self):
        return { 
            'category': self.category,
            'code': self.code,
            'status': self.status,
            'details': self.details,
            'correlation_id': self.correlation_id,
            'message': self.message,
            'cause': str(self.cause),
            'stack_stace': self.stack
        }
        
    def get_cause_string(self):
        return str(self.cause)

    def set_cause_string(self, value):
        self.cause = value

    def get_stack_trace_string(self):
        if (self.stack_trace != None):
            return self.stack_trace
        # elif (hasattr(self, 'tb_frame')):
        #     return traceback.format_tb(self)
        else:
            return None

    def set_stack_trace_string(self, value):
        self.stack_trace = value

    def with_code(self, code):
        self.code = code if code != None else 'UNKNOWN'
        self.name = code
        return self
        
    def with_status(self, status):
        self.status = status if status != None else 500
        return self
        
    def with_details(self, key, value):
        self.details = self.details if self.details != None else {}
        self.details[key] = value
        return self
        
    def with_cause(self, cause):
        self.cause = cause
        return self
        
    def with_correlation_id(self, correlation_id):
        self.correlation_id = correlation_id
        return self
                
    def wrap(self, cause):
        if isinstance(cause, ApplicationException):
            return cause
            
        self.with_cause(cause)
        return self

    @staticmethod
    def wrap_exception(exception, cause):
        if isinstance(cause, ApplicationException):
            return cause
        
        exception.with_cause(cause)
        return exception
            
    @staticmethod
    def from_value(value):
        value = value if isinstance(value, dict) else dict(value)

        error = MicroserviceError(
            value['category'] if 'category' in value else None,
            value['correlation_id'] if 'correlation_id' in value else None,
            value['code'] if 'code' in value else None,
            value['message'] if 'message' in value else None
        ).with_status(value['status'])

        if 'cause' in value:
            error.with_cause(value['cause'])
        if 'details' in value:
            error.with_details(value['details'])
        if 'stack_trace' in value:
            error.with_stack(value['stack_trace'])

        return error