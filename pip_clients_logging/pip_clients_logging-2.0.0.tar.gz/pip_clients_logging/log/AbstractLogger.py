# -*- coding: utf-8 -*-
"""
    pip_clients_logging.log.AbstractLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading
import socket

from pip_services_commons.log import ILogger, Logger
from pip_services_commons.errors import ErrorDescriptionFactory
from pip_services_commons.config import IReconfigurable
from pip_services_commons.refer import IReferences, IReferenceable
from pip_services_commons.run import IOpenable

from ..version1.LogMessageV1 import LogMessageV1

class AbstractLogger(Logger, IReconfigurable, IReferenceable, IOpenable):
    _client = None
    _cache = None
    _updated = None
    _last_dump_time = None
    _interval = 1000
    _lock = None


    def __init__(self, client):
        super(AbstractLogger, self).__init__()
        self._cache = []
        self._updated = False
        self._last_dump_time = time.clock() * 1000
        self._lock = threading.Lock()
        self._client = client


    def configure(self, config):
        self._interval = config.get_as_integer_with_default("interval", self._interval)
        self._client.configure(config)
	
    def set_references(self, references):
        self._client.set_references(references)

    def is_opened(self):
        return self._client.is_opened()

    def open(self, correlation_id):
        self._client.open(correlation_id)

    def close(self, correlation_id):
        self._client.close(correlation_id)


    def _write(self, level, correlation_id, ex, message):
        error = ErrorDescriptionFactory.create(ex) if ex != None else None
        source = socket.gethostname() # Todo: add process/module name
        log_message = LogMessageV1(level, source, correlation_id, error, message)
        
        self._lock.acquire()
        try:
            self._cache.append(log_message)
        finally:
            self._lock.release()

        # Todo: Find out how to debounc
        self._update()


    def clear(self):
        self._lock.acquire()
        try:
            self._cache = []
            self._updated = False
        finally:
            self._lock.release()


    def dump(self):
        if self._updated:
            self._lock.acquire()
            try:
                if not self._updated:
                    return
                
                messages = self._cache                
                self._client.write_messages("logger", messages)
                self._cache = []

                self._updated = False
                self._last_dump_time = time.clock() * 1000
            finally:
                self._lock.release()


    def _update(self):
        self._updated = True
        current_time = time.clock() * 1000
        
        if current_time > self._last_dump_time + self._interval:
            try:
                self.dump()
            except:
                # Todo: decide what to do
                pass
