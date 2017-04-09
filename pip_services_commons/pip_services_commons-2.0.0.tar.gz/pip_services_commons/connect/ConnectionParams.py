# -*- coding: utf-8 -*-
"""
    pip_services_common.connect.ConnectionParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Connection parameters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..config.ConfigParams import ConfigParams

class ConnectionParams(ConfigParams):
    """
    Connection parameters as set in component configuration or retrieved by discovery service. 
    It contains service protocol, host, port number, route, database name, timeouts 
    and additional configuration parameters.
    """

    def __init__(self, map = None):
        """
        Create an instance of service address with free-form configuration map.

        Args:
            content: a map with the address configuration parameters.
        """
        super(ConnectionParams, self).__init__(map)

    def use_discovery(self):
        """
        Checks if discovery registration or resolution shall be performed.
        The discovery is requested when 'discover' parameter contains
        a non-empty string that represents the discovery name.

        Returns: True if the address shall be handled by discovery
                 and False when all address parameters are defined statically.
        """
        return "discovery_key" in self

    def get_discovery_key(self):
        """
        Gets a key under which the connection shall be registered or resolved by discovery service.
        Returns: a key to register or resolve the connection
        """
        return self.get_as_nullable_string("discovery_key")

    def set_discovery_key(self, value):
        """
        Sets the key under which the connection shall be registered or resolved by discovery service

        Args:
            value: a key to register or resolve the connection
        """
        self.put("discovery_key", value)

    def get_protocol(self):
        """
        Gets the connection protocol
        Returns: the connection protocol
        """
        return self.get_as_nullable_string("protocol")

    def get_protocol(self, default_value = None):
        """
        Gets the connection protocol

        Args:
            default_value: the default protocol

        Returns: the connection protocol
        """
        return self.get_as_string_with_default("protocol", default_value)

    def set_protocol(self, value):
        """
        Sets the connection protocol

        Args:
            value: the connection protocol
        """
        self.put("protocol", value)

    def get_host(self):
        """
        Gets the service host name or IP address.
        Returns: a string representing service host
        """
        host = self.get_as_nullable_string("host")
        host = host if host != None else self.get_as_nullable_string("ip")
        return host

    def set_host(self, value):
        """
        Sets the service host name or IP address.

        Args:
            value: a string representing service host
        """
        self.put("host", value)

    def get_port(self):
        """
        Gets the service port number
        Returns: integer representing the service port.
        """
        return self.get_as_integer("port")

    def set_port(self, value):
        """
        Sets the service port number

        Args:
            value: integer representing the service port.
        """
        self.set_as_object("port", value)

    def get_uri(self):
        """
        Gets the endpoint uri constructed from protocol, host and port
        Returns: uri
        """
        return self.get_as_string("uri")

    def set_uri(self, value):
        """
        Sets the endpoint uri

        Args:
            value: string connection uri
        """
        self.set_as_object("uri", value)

    @staticmethod
    def from_string(line):
        map = StringValueMap.from_string(line)
        return ConnectionParams(map)

    @staticmethod
    def many_from_config(config):
        result = []

        # Try to get multiple connections first
        connections = config.get_section("connections")
        if len(connections) > 0:
            sections_names = connections.get_section_names()
            for section in sections_names:
                connection = connections.get_section(section)
                result.append(ConnectionParams(connection))
        # Then try to get a single connection
        else:
            connection = config.get_section("connection")
            result.append(ConnectionParams(connection))

        return result

    @staticmethod
    def from_config(config):
        connections = ConnectionParams.many_from_config(config)
        return connections[0] if len(connections) > 0 else None
