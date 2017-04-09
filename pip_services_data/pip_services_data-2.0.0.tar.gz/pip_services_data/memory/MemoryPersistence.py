# -*- coding: utf-8 -*-
"""
    pip_services_data.memory.MemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import threading

from pip_services_commons.refer import IReferenceable
from pip_services_commons.config import IReconfigurable
from pip_services_commons.run import IOpenable, IClosable, ICleanable
from pip_services_commons.log import CompositeLogger
from pip_services_commons.data import PagingParams, DataPage, IdGenerator

class MemoryPersistence(object, IReferenceable, IOpenable, ICleanable):
    _logger = None
    _items = None
    _loader = None
    _saver = None
    _lock = None
    _opened = False

    def __init__(self, loader = None, saver = None):
        self._lock = threading.Lock()
        self._logger = CompositeLogger()
        self._items = []
        self._loader = loader
        self._saver = saver

    def set_references(self, references):
        self._logger.set_references(references)

    def is_opened(self):
        return self._opened

    def open(self, correlation_id):
        self.load(correlation_id)
        self._opened = True

    def close(self, correlation_id):
        self.save(correlation_id)
        self._opened = False

    def _convert_to_public(self, value):
        return value

    def _convert_from_public(self, value):
        return value

    def load(self, correlation_id):
        if self._loader == None: return

        self._lock.acquire()
        try:
            items = self._loader.load(correlation_id)
            self._items = []
            for item in items:
                item = self._convert_to_public(item)
                self._items.append(item)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Loaded " + str(len(self._items)) + " items")

    def save(self, correlation_id):
        if self._saver == None: return

        self._lock.acquire()
        try:
            items = []
            for item in self._items:
                item = self._convert_from_public(item)
                items.append(item)
            self._saver.save(correlation_id, items)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Saved " + str(len(self._items)) + " items")

    def clear(self, correlation_id):
        self._lock.acquire()
        
        try:
            del self._items[:]
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Cleared items")

        # Outside of lock to avoid reentry
        self.save(correlation_id)
