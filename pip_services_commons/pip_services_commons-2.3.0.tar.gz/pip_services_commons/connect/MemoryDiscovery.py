# -*- coding: utf-8 -*-
"""
    pip_services_common.connect.MemoryDiscovery
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory discovery implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..config.ConfigParams import ConfigParams
from ..config.IReconfigurable import IReconfigurable
from .IDiscovery import IDiscovery
from .ConnectionParams import ConnectionParams

class DiscoveryItem:
    key = None
    connection = None

class MemoryDiscovery(object, IDiscovery, IReconfigurable):
    _items = None

    def __init__(self, config = None):
        self._items = []
        if config != None:
            self.configure(config)

    def configure(self, config):
        self.read_connections(config)

    def read_connections(self, connections):
        del self._items[:]
        for key in connections.get_key_names():
            item = DiscoveryItem()
            item.key = key
            value = connections.get_as_nullable_string(key)
            item.connection = ConnectionParams.from_string(value)
            self._items.append(item)

    def register(self, correlation_id, key, connection):
        item = DiscoveryItem()
        item.key = key
        item.connection = connection
        self._items.append(item)

    def resolve_one(self, correlation_id, key):
        connection = None
        for item in self._items:
            if item.key == key and item.connection != None:
                connection = item.connection
                break
        return connection

    def resolve_all(correlationId, key):
        connections = []
        for item in self._items:
            if item.key == key and item.connection != None:
                connections.append(item.connection)
        return connections
