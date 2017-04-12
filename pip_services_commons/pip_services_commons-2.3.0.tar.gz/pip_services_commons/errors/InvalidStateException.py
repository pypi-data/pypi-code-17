# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.InvalidStateException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    InvalidState exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class InvalidStateException(ApplicationException):
    """
    Errors related to operations called in wrong component state.
    For instance, business calls when component is not ready
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(InvalidStateException, self).__init__(ErrorCategory.InvalidState, correlation_id, code, message)
        self.status = 500
