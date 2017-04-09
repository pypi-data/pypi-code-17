# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.BadRequestException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    BadRequest exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class BadRequestException(ApplicationException):
    """
    Errors due to improper user requests, like missing or wrong parameters 
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(BadRequestException, self).__init__(ErrorCategory.BadRequest, correlation_id, code, message)
        self.status = 400
