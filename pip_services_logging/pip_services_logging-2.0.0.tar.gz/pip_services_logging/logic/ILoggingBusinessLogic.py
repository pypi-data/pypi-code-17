# -*- coding: utf-8 -*-
"""
    pip_services_logging.logic.ILoggingBusinessLogic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging business logic interface
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.run import ICleanable

class ILoggingBusinessLogic(ICleanable):
    def read_messages(self, correlation_id, filter, paging):
        raise NotImplementedError('Method from interface definition')

    def read_errors(self, correlation_id, filter, paging):
        raise NotImplementedError('Method from interface definition')

    def write_message(self, correlation_id, message):
        raise NotImplementedError('Method from interface definition')
    
    def write_messages(self, correlation_id, messages):
        raise NotImplementedError('Method from interface definition')

    def clear(self, correlation_id):
        raise NotImplementedError('Method from interface definition')
