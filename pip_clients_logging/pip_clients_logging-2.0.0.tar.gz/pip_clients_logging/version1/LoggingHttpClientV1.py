# -*- coding: utf-8 -*-
"""
    pip_clients_logging.version1.LoggingHttpClientV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Http logging client implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.data import DataPage
from pip_services_commons.config import ConfigParams
from pip_services_net.rest import CommandableHttpClient

from .ILoggingClientV1 import ILoggingClientV1
from .LogMessageV1 import LogMessageV1

class LoggingHttpClientV1(CommandableHttpClient, ILoggingClientV1):

    def __init__(self, config = None):
        super(LoggingHttpClientV1, self).__init__('logging')
        if config != None:
            self.configure(ConfigParams.from_value(config))

    def _datapage_to_public(self, page):
        if not isinstance(page, dict): return page

        data = []
        for item in page['data']:
            item = LogMessageV1.from_json(item)
            data.append(item)
        total = page['total'] if 'total' in page else None

        return DataPage(data, total)


    def read_messages(self, correlation_id, filter, paging):
        page = self.call_command(
            'read_messages',
            correlation_id,
            {
                'filter': filter,
                'paging': paging
            }
        )
        return self._datapage_to_public(page)


    def read_errors(self, correlation_id, filter, paging):
        page = self.call_command(
            'read_errors',
            correlation_id,
            {
                'filter': filter,
                'paging': paging
            }
        )
        return self._datapage_to_public(page)


    def write_message(self, correlation_id, message):
        page = self.call_command(
            'write_message',
            correlation_id,
            {
                'message': message
            }
        )
        return LogMessageV1.from_json(page)


    def write_messages(self, correlation_id, messages):
        page = self.call_command(
            'write_messages',
            correlation_id,
            {
                'messages': messages
            }
        )


    def clear(self, correlation_id):
        self.call_command(
            'clear',
            correlation_id,
            { }
        )
