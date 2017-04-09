# -*- coding: utf-8 -*-
"""
    pip_services_data.memory.IdentifiableMemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Identifiable memory persistence implementation
    
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

from .MemoryPersistence import MemoryPersistence

# This function will be overriden in the code
filtered = filter

class IdentifiableMemoryPersistence(MemoryPersistence, IReconfigurable):
    _max_page_size = 100

    def __init__(self, loader = None, saver = None):
        super(IdentifiableMemoryPersistence, self).__init__(loader, saver)

    def configure(self, config):
        self._max_page_size = config.get_as_integer_with_default("options.max_page_size", self._max_page_size)

    def get_page_by_filter(self, correlation_id, filter, paging, sort = None, select = None):
        self._lock.acquire()
        try:
            items = list(self._items)
        finally:
            self._lock.release()
            
        # Filter and sort
        if filter != None:
            items = filtered(filter, items)
        if sort != None:
            items = sorted(items, sort)

        # Prepare paging parameters
        paging = paging if paging != None else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        
        # Get a page
        data = items
        if skip > 0:
            data = data[skip:]
        if take > 0:
            data = data[:take+1]
                
        # Convert values
        if select != None:
            data = map(select, data)
                
        self._logger.trace(correlation_id, "Retrieved " + str(len(data)) + " items")

        # Return a page
        return DataPage(data, len(items))

    def get_list_by_filter(self, correlation_id, filter, sort = None, select = None):
        self._lock.acquire()
        try:
            items = list(self._items)
        finally:
            self._lock.release()

        # Filter and sort
        if filter != None:
            items = filtered(items, filter)
        if sort != None:
            items = sorted(items, sort) 
                        
        # Convert values      
        if select != None:
            items = map(select, items)
                
        # Return a list
        return items

    def _find_one(self, id):
        for item in self._items:
            if item['id'] == id:
                return item
        return None

    def get_one_by_id(self, correlation_id, id):
        self._lock.acquire()
        try:
            item = self._find_one(id)
        finally:
            self._lock.release()

        if item != None:
            self._logger.trace(correlation_id, "Retrieved " + str(item) + " by " + str(id))
        else:
            self._logger.trace(correlation_id, "Cannot find item by " + str(id))
        return item

    def get_one_random(self, correlation_id):
        self._lock.acquire()
        try:
            if len(self._items) == 0:
                return None

            index = random.randint(0, len(self._items))
            item = self._items[index]
        finally:
            self._lock.release()
            
        if item != None:
            self._logger.trace(correlation_id, "Retrieved a random item")
        else:
            self._logger.trace(correlation_id, "Nothing to return as random item")
                        
        return item

    def create(self, correlation_id, item):
        if 'id' not in item or item['id'] == None:
            item['id'] = IdGenerator.next_long()

        self._lock.acquire()
        try:
            self._items.append(item)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Created " + str(item))

        # Avoid reentry
        self.save(correlation_id)
        return item


    def set(self, correlation_id, new_item):
        if 'id' not in item or item['id'] == None:
            item['id'] = IdGenerator.next_long()

        self._lock.acquire()
        try:
            old_item = self._find_one(new_item['id'])
            if old_item == None:
                self._items.append(new_item)
            else:
                index = self._items.index(old_item)
                if index < 0:
                    self._items.append(new_item)
                else:
                    self._items[index] = new_item
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Set " + str(new_item))

        # Avoid reentry
        self.save(correlation_id)
        return new_item


    def update(self, correlation_id, new_item):
        self._lock.acquire()
        try:
            old_item = self._find_one(new_item['id'])
            if old_item == None:
                return None
            
            index = self._items.index(old_item)
            if index < 0: return None

            self._items[index] = new_item
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Updated " + str(new_item))

        # Avoid reentry
        self.save(correlation_id)
        return new_item


    def update_partially(self, correlation_id, id, data):
        new_item = None

        self._lock.acquire()
        try:
            old_item = self._find_one(id)
            if old_item == None:
                return None
            
            for (k, v) in data.items():
                old_item[k] = v

            new_item = old_item
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Partially updated " + str(old_item))

        # Avoid reentry
        self.save(correlation_id)
        return new_item

    def delete_by_id(self, correlation_id, id):
        self._lock.acquire()
        try:
            item = self._find_one(id)
            if item == None: return None
            
            index = self._items.index(item)
            if index < 0: return None

            del self._items[index]
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Deleted " + str(item))

        self.save(correlation_id)
        return item
