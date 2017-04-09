# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.ConflictException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Conflict exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class ConflictException(ApplicationException):
    """
    Errors raised by conflict in object versions posted by user and stored on server.
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(ConflictException, self).__init__(ErrorCategory.Conflict, correlation_id, code, message)
        self.status = 409
