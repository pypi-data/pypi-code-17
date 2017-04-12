# -*- coding: utf-8 -*-
"""
    pip_services_common.connect.ConnectionResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Connection resolver implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConnectionParams import ConnectionParams
from .IDiscovery import IDiscovery
from ..config.IConfigurable import IConfigurable
from ..refer.IReferenceable import IReferenceable
from ..refer.Descriptor import Descriptor
from ..errors.ConfigException import ConfigException

class ConnectionResolver(object, IConfigurable, IReferenceable):
    _connections = None
    _references = None

    def __init__(self, config = None, references = None):
        self._connections = []
        if config != None:
            self.configure(config)
        if references != None:
            self.set_references(references)

    def set_references(self, references):
        self._references = references

    def configure(self, config):
        connections = ConnectionParams.many_from_config(config)
        for connection in connections:
            self._connections.append(connection)

    def get_all(self):
        return self._connections

    def add(self, connection):
        self._connections.add(connection)

    def _register_in_discovery(self, correlation_id, connection):
        if connection.use_discovery() == False: return False
        
        key = connection.get_discovery_key()
        if self._references == None:
            return False
        
        descriptor = Descriptor("*", "discovery", "*", "*", "*")
        components = self._references.get_optional(descriptor)
        if components == None:
            return False
        
        for component in components:
            if isinstance(component, IDiscovery):
                component.register(correlation_id, key, connection)
        
        return True

    def register(self, correlation_id, connection):
        result = self._register_in_discovery(correlation_id, connection)
        
        if result:
            self._connections.append(connection)

    def _resolve_in_discovery(self, correlation_id, connection):
        if connection.use_discovery() == False: return None
        
        key = connection.get_discovery_key()
        descriptor = Descriptor("*", "discovery", "*", "*")
        components = self._references.get_optional(descriptor)
        if len(components) == 0:
            raise ConfigException(correlation_id, "CANNOT_RESOLVE", "Discovery wasn't found to make resolution")

        for component in components:
            if isinstance(component, IDiscovery):
                resolved_connection = component.resolve_one(correlation_id, key)
                if resolved_connection != None:
                    return resolved_connection
        
        return None

    def resolve(self, correlation_id):
        if len(self._connections) == 0: return None
        
        # Return connection that doesn't require discovery
        for connection in self._connections:
            if not connection.use_discovery():
                return connection
        
        # Return connection that require discovery
        for connection in self._connections:
            if connection.use_discovery():
                resolved_connection = self._resolve_in_discovery(correlation_id, connection)
                if resolved_connection != None:
                    # Merge configured and new parameters
                    resolved_connection = ConnectionParams(ConfigParams.merge_configs(connection, resolved_connection))
                    return resolved_connection
        
        return None

    def _resolve_all_in_discovery(self, correlation_id, connection):
        result = []
        
        if connection.use_discovery() == False: return result
        
        key = connection.get_discovery_key()
        descriptor = Descriptor("*", "discovery", "*", "*")
        components = self._references.get_optional(descriptor)
        if len(components) == 0:
            raise ConfigException(correlation_id, "CANNOT_RESOLVE", "Discovery wasn't found to make resolution")

        for component in components:
            if isinstance(component, IDiscovery):
                resolved_connections = component.resolve_all(correlation_id, key)
                if resolved_connections != None:
                    for connection in resolved_connections:
                        result.append(connection)
        
        return result

    def resolve_all(self, correlation_id):
        resolved = []
        to_resolve = []

        # Sort connections
        for connection in self._connections:
            if connection.use_discovery():
                to_resolve.append(connection)
            else:
                resolved.append(connection)
        
        # Resolve addresses that require that
        if len(to_resolve) > 0:
            for connection in to_resolve:
                resolved_connections = self._resolve_all_in_discovery(correlation_id, connection)
                for resolved_connection in resolved_connections:
                    # Merge configured and new parameters
                    resolved_connection = ConnectionParams(ConfigParams.merge_configs(connection, resolved_connection))
                    resolved.append(resolved_connection)
        
        return resolved
