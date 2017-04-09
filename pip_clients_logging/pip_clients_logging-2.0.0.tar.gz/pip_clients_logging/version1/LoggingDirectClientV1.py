# -*- coding: utf-8 -*-
"""
    pip_clients_logging.version1.LoggingDirectClientV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Direct logging client implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.data import DataPage
from pip_services_commons.refer import Descriptor
from pip_services_net.direct import DirectClient

from .ILoggingClientV1 import ILoggingClientV1

class LoggingDirectClientV1(DirectClient, ILoggingClientV1):

    def __init__(self):
        super(LoggingDirectClientV1, self).__init__()
        self._dependency_resolver.put('controller', Descriptor("pip-services-logging", "controller", "*", "*", "*"))


    def read_messages(self, correlation_id, filter, paging):
        timing = self._instrument(correlation_id, 'logging.read_messages')
        try:
            return self._controller.read_messages(correlation_id, filter, paging)
        finally:
            timing.end_timing()


    def read_errors(self, correlation_id, filter, paging):
        timing = self._instrument(correlation_id, 'logging.read_errors')
        try:
            return self._controller.read_errors(correlation_id, filter, paging)
        finally:
            timing.end_timing()


    def write_message(self, correlation_id, message):
        timing = self._instrument(correlation_id, 'logging.write_message')
        try:
            return self._controller.write_message(correlation_id, message)
        finally:
            timing.end_timing()


    def write_messages(self, correlation_id, messages):
        timing = self._instrument(correlation_id, 'logging.write_messages')
        try:
            self._controller.write_messages(correlation_id, messages)
        finally:
            timing.end_timing()


    def clear(self, correlation_id):
        timing = self._instrument(correlation_id, 'logging.clear')
        try:
            return self._controller.clear(correlation_id)
        finally:
            timing.end_timing()

