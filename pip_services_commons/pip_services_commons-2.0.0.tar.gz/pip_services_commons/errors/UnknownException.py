# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.UnknownException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Unknown exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class UnknownException(ApplicationException):
    """
    Unknown or unexpected errors
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(UnknownException, self).__init__(ErrorCategory.Unknown, correlation_id, code, message)
        self.status = 500
