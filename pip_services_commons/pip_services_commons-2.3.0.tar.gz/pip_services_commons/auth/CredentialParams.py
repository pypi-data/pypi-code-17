# -*- coding: utf-8 -*-
"""
    pip_services_common.auth.CredentialParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Credential parameters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..config.ConfigParams import ConfigParams

class CredentialParams(ConfigParams):
    """
    Credentials such as login and password, client id and key,
    certificates, etc. Separating credentials from connection parameters
    allow to store them in secure location and share among multiple connections.
    """

    def __init__(self, map = None):
        """
        Creates an empty instance of credential parameters.

        Args:
            map: content a map with the credentials. 
        """
        super(CredentialParams, self).__init__(map)

    def use_credential_store(self):
        """
        Checks if credential lookup shall be performed.
        The credentials are requested when 'store_key' parameter contains
        a non-empty string that represents the name in credential store.

        Returns: True if the credentials shall be resolved by credential store
                 and false when all credential parameters are defined statically.
        """
        return "store_key" in self

    def get_store_key(self):
        """
        Gets a key under which the connection shall be looked up in credential store.
        Returns: a credential key 
        """
        return self.get_as_nullable_string("store_key")

    def set_store_key(self, value):
        """
        Sets the key under which the credentials shall be looked up in credential store

        Args:
            value: a new credential key
        """
        self.put("store_key", value)

    def get_username(self):
        """
        Gets the user name / login.
        Returns: the user name
        """
        username = self.get_as_nullable_string("username")
        username = username if username != None else self.get_as_nullable_string("user")
        return username

    def set_username(self, value):
        """
        Sets the service user name.

        Args:
            value: the user name
        """
        self.put("username", value)

    def get_password(self):
        """
        Gets the service user password.
        Returns: the user password
        """
        password = self.get_as_nullable_string("password")
        password = password if password != None else self.get_as_nullable_string("pass")
        return password

    def set_password(self, password):
        """
        Sets the service user password.

        Args:
            password: the user password
        """
        self.put("password", password)

    def get_access_id(self):
        """
        Gets the client or access id
        Returns: the client or access id
        """
        access_id = self.get_as_nullable_string("access_id")
        access_id = access_id if access_id != None else self.get_as_nullable_string("client_id")
        return access_id

    def set_access_id(self, value):
        """
        Sets a new client or access id

        Args:
            value: the client or access id
        """
        self.put("access_id", value)

    def get_access_key(self):
        """
        Gets the client or access key
        Returns: the client or access key
        """
        access_key = self.get_as_nullable_string("access_key")
        access_key = access_key if access_key != None else self.get_as_nullable_string("access_key")
        return access_key

    def set_access_key(self, value):
        """
        Sets a new client or access key

        Args:
            value: the client or access id
        """
        self.put("access_key", value)

    @staticmethod
    def from_string(line):
        map = StringValueMap.from_string(line)
        return CredentialParams(map)

    @staticmethod
    def many_from_config(config):
        result = []

        # Try to get multiple credentials first
        credentials = config.get_section("credentials")
        if len(credentials) > 0:
            sections_names = credentials.get_section_names()
            for section in sections_names:
                credential = credentials.get_section(section)
                result.append(CredentialParams(credential))
        # Then try to get a single credential
        else:
            credential = config.get_section("credential")
            result.append(CredentialParams(credential))

        return result

    @staticmethod
    def from_config(config):
        credentials = CredentialParams.many_from_config(config)
        return credentials[0] if len(credentials) > 0 else None
