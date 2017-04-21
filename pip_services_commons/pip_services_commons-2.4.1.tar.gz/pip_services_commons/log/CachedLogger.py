# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.CachedLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cached logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading
import socket

from .ILogger import ILogger
from .Logger import Logger
from .LogMessage import LogMessage
from ..errors.ErrorDescriptionFactory import ErrorDescriptionFactory
from ..config.IReconfigurable import IReconfigurable

class CachedLogger(Logger, IReconfigurable):
    _cache = None
    _updated = None
    _last_dump_time = None
    _interval = 60000
    _lock = None


    def __init__(self):
        self._cache = []
        self._updated = False
        self._last_dump_time = time.clock() * 1000
        self._lock = threading.Lock()


    def _write(self, level, correlation_id, ex, message):
        error = ErrorDescriptionFactory.create(ex) if ex != None else None
        source = socket.gethostname() # Todo: add process/module name
        log_message = LogMessage(level, source, correlation_id, error, message)
        
        self._lock.acquire()
        try:
            self._cache.append(log_message)
        finally:
            self._lock.release()

        self._update()


    def _save(messages):
        raise NotImplementedError('Method from abstract implementation')


    def configure(self, config):
        self._interval = config.get_as_float_with_default("interval", self._interval)


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
                self._cache = []
                
                self._save(messages)

                self._updated = False
                self._last_dump_time = time.clock() * 1000
            finally:
                self._lock.release()


    def _update(self):
        self._updated = True
        
        if time.clock() * 1000 > self._last_dump_time + self._interval:
            try:
                self.dump()
            except:
                # Todo: decide what to do
                pass
