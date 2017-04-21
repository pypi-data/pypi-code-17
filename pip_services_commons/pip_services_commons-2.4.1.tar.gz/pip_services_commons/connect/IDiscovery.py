# -*- coding: utf-8 -*-
"""
    pip_services_common.connect.IDicovery
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Discovery service interface
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConnectionParams import ConnectionParams

class IDiscovery:
    """
    Service discovery component used to register connections of the services
    or to resolve connections to external services called by clients.
    """

    def register(self, correlation_id, key, connection):
        """
        Registers connection where API service binds to.

        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: a key to identify the connection
            connection: the connection to be registered.
        """
        raise NotImplementedError('Method from interface definition')

    def resolve_one(self, correlation_id, key):
        """
        Resolves one connection from the list of service connections.
        
        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: a key locate a connection

        Returns: a resolved connection.
        """
        raise NotImplementedError('Method from interface definition')

    def resolve_all(self, correlation_id, key):
        """
        Resolves a list of connections from to be called by a client.

        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: a key locate connections

        Returns: a list with resolved connections.
        """
        raise NotImplementedError('Method from interface definition')
