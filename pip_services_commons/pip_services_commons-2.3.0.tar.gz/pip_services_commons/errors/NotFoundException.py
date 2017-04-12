# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.NotFoundException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    NotFound exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class NotFoundException(ApplicationException):
    """
    Error caused by attempt to access missing object
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(NotFoundException, self).__init__(ErrorCategory.NotFound, correlation_id, code, message)
        self.status = 404
