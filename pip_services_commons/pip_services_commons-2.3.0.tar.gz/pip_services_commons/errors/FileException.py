# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.FileException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    File exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class FileException(ApplicationException):
    """
    File or unexpected errors
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(FileException, self).__init__(ErrorCategory.FileError, correlation_id, code, message)
        self.status = 500
