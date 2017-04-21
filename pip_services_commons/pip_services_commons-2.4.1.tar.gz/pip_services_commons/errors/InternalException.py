# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.InternalException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Internal exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class InternalException(ApplicationException):
    """
    Errors caused by programming mistakes
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(InternalException, self).__init__(ErrorCategory.Internal, correlation_id, code, message)
        self.status = 500
