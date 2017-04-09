# -*- coding: utf-8 -*-
"""
    pip_clients_logging.version1.LoggingNullClientV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null logging client implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.data import DataPage

from .ILoggingClientV1 import ILoggingClientV1

class LoggingNullClientV1(object, ILoggingClientV1):

    def read_messages(self, correlation_id, filter, paging):
        return DataPage([], 0)

    def read_errors(self, correlation_id, filter, paging):
        return DataPage([], 0)

    def write_message(self, correlation_id, message):
        return message
    
    def write_messages(self, correlation_id, messages):
        pass

    def clear(self, correlation_id):
        pass
