# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.UnauthorizedException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Unauthorized exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class UnauthorizedException(ApplicationException):
    """
    Access errors caused by missing user identity or security permissions
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(UnauthorizedException, self).__init__(ErrorCategory.Unauthorized, correlation_id, code, message)
        self.status = 401
