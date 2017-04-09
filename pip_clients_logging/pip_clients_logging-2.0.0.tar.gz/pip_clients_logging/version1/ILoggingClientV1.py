# -*- coding: utf-8 -*-
"""
    pip_clients_logging.version1.ILoggingClientV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging client interface for version1
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.run import ICleanable

class ILoggingClientV1(ICleanable):
    
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
