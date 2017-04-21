# -*- coding: utf-8 -*-
"""
    pip_services_common.auth.MemoryCredentialStore
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory credential store implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..config.ConfigParams import ConfigParams
from ..config.IReconfigurable import IReconfigurable
from ..data.StringValueMap import StringValueMap
from .ICredentialStore import ICredentialStore
from .CredentialParams import CredentialParams

class MemoryCredentialStore(object, ICredentialStore, IReconfigurable):
    _items = None

    def __init__(self, credentials = None):
        self._items = StringValueMap()
        if credentials != None:
            self.configure(credentials)

    def configure(self, config):
        self.read_credentials(config)

    def read_credentials(self, credentials):
        self._items.clear()
        for key in credentials.get_key_names():
            value = credentials.get_as_nullable_string(key)
            self._items.append(key, CredentialParams.from_tuples([key, value]))

    def store(self, correlation_id, key, credential):
        if credential != null:
            self._items.put(key, credential)
        else:
            self._items.remove(key)

    def lookup(correlation_id, key):
        credential = self._items.get_as_object(key)
