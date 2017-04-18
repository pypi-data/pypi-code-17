# -*- coding: utf-8 -*-
"""
    pip_services_commons.errors.ApplicationExceptionFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Application exception factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException
from .UnknownException import UnknownException
from .InternalException import InternalException
from .ConfigException import ConfigException
from .InvalidStateException import InvalidStateException
from .ConnectionException import ConnectionException
from .InvocationException import InvocationException
from .FileException import FileException
from .BadRequestException import BadRequestException
from .NotFoundException import NotFoundException
from .UnauthorizedException import UnauthorizedException
from .ConflictException import ConflictException
from .UnsupportedException import UnsupportedException

class ApplicationExceptionFactory(object):

    @staticmethod
    def create(description):
        error = None
        
        # Create well-known exception type based on error category
        if ErrorCategory.Unknown == description.category:
            error = UnknownException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.Internal == description.category:
            error = InternalException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.Misconfiguration == description.category:
            error = ConfigException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.NoResponse == description.category:
            error = ConnectionException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.FailedInvocation == description.category:
            error = InvocationException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.FileError == description.category:
            error = FileException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.BadRequest == description.category:
            error = BadRequestException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.Unauthorized == description.category:
            error = UnauthorizedException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.Conflict == description.category:
            error = ConflictException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.NotFound == description.category:
            error = NotFoundException(description.correlation_id, description.code, description.message)
        elif ErrorCategory.Unsupported == description.category:
            error = UnsupportedException(description.correlation_id, description.code, description.message)
        else:
            error = UnknownException()
            error.category = description.category
            error.status = description.status
        
        # Fill error with details
        error.details = description.details
        error.set_cause_string(description.cause)
        error.set_stack_trace_string(description.stack_trace)
        
        return error
