# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.ConfigException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Config exception type
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .ApplicationException import ApplicationException

class ConfigException(ApplicationException):
    """
    Errors related to mistakes in microservice user-defined configuration
    """

    def __init__(self, correlation_id = None, code = None, message = None):
        super(ConfigException, self).__init__(ErrorCategory.Misconfiguration, correlation_id, code, message)
        self.status = 500
