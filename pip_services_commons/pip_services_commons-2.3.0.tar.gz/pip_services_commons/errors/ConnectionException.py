# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.ConnectionException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Connection exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class ConnectionException(ApplicationException):
    """
    Errors happened during connection to remote services.
    They can be related to misconfiguration, network issues
    or remote service itself 
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(ConnectionException, self).__init__(ErrorCategory.NoResponse, correlation_id, code, message)
        self.status = 500
