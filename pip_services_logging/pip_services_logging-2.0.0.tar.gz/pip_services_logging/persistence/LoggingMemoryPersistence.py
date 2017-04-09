# -*- coding: utf-8 -*-
"""
    pip_services_logging.persistence.LoggingMemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading

from pip_services_commons.run import ICleanable
from pip_services_commons.config import ConfigParams, IConfigurable
from pip_services_commons.data import FilterParams, PagingParams, DataPage
from pip_services_commons.log import LogLevel
from pip_services_commons.convert import DateTimeConverter

from .ILoggingPersistence import ILoggingPersistence

class LoggingMemoryPersistence(object, ILoggingPersistence, IConfigurable):
    _max_page_size = 100
    _max_error_size = 1000
    _max_total_size = 10000

    _lock = None
    _messages = None
    _errors = None

    def __init__(self):
        self._lock = threading.Lock()
        self._messages = []
        self._errors = []


    def configure(self, config):
        self._max_page_size = config.get_as_integer_with_default('options.max_page_size', self._max_page_size)
        self._max_error_size = config.get_as_integer_with_default('options.max_error_size', self._max_error_size)
        self._max_total_size = config.get_as_integer_with_default('options.max_total_size', self._max_total_size)


    def _match_string(self, value, search):
        if value == None and search == None:
            return True
        if value == None or search == None:
            return False
        return search in value.lower()


    def _message_contains(self, message, search):
        search = search.lower()

        if self._match_string(message.message, search):
            return True
        if self._match_string(message.correlation_id, search):
            return True

        if message.error != None:
            if self._match_string(message.error.message, search):
                return True
            if self._match_string(message.error.stack_trace, search):
                return True
            if self._match_string(message.error.code, search):
                return True

        return False


    def get_page_by_filter(self, correlation_id, filter, paging):
        filter = filter if filter != None else FilterParams()
        search = filter.get_as_nullable_string("search")
        level = filter.get_as_nullable_integer("level")
        max_level = filter.get_as_nullable_integer("max_level")
        from_time = filter.get_as_nullable_datetime("from_time")
        to_time = filter.get_as_nullable_datetime("to_time")
        errors_only = filter.get_as_boolean_with_default("errors_only", False)

        paging = paging if paging != None else PagingParams()
        skip = paging.get_skip(0)
        take = paging.get_take(self._max_page_size)
        data = []

        self._lock.acquire()
        try:
            messages = self._errors if errors_only else self._messages
            for message in messages:
                message_time = DateTimeConverter.to_utc_datetime(message.time)

                if search != None and not self._message_contains(message, search):
                    continue
                if level != None and level != message.level:
                    continue
                if max_level != None and max_level < message.level:
                    continue
                if from_time != None and from_time > message_time:
                    continue
                if to_time != None and to_time <= message_time:
                    continue

                skip -= 1
                if skip >= 0: continue

                data.append(message)

                take -= 1
                if take <= 0: break
        finally:
            self._lock.release()

        total = len(data)
        return DataPage(data, total)


    def _truncate_messages(self, messages, max_size):
        # Remove messages from the end
        if len(messages) > max_size:
            messages = messages[0:max_size]
        return messages


    def _insert_message(self, message, messages):
        index = 0
        # Find index to keep messages sorted by time
        while index < len(messages):
            if message.time >= messages[index].time:
                break
            index += 1
        
        if index < len(messages):
            messages.insert(index, message)
        else:
            messages.append(message)
        
        return messages


    def create(self, correlation_id, message):
        self._lock.acquire()
        try:
            # Add to all messages
            self._messages = self._truncate_messages(self._messages, self._max_total_size)
            self._messages = self._insert_message(message, self._messages)

            # Add to errors separately
            if message.level <= LogLevel.Error:
                self._errors = self._truncate_messages(self._errors, self._max_error_size)
                self._errors = self._insert_message(message, self._errors)
        finally:
            self._lock.release()

        return message


    def clear(self, correlation_id):
        self._lock.acquire()
        try:
            self._messages = []
            self._errors = []
        finally:
            self._lock.release()
