# -*- coding: utf-8 -*-
"""
    pip_services_common.auth.CredentialResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Credential resolver implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .CredentialParams import CredentialParams
from ..refer.Descriptor import Descriptor
from .ICredentialStore import ICredentialStore
from ..config.IConfigurable import IConfigurable
from ..refer.IReferenceable import IReferenceable
from ..refer.ReferenceException import ReferenceException
from ..errors.ApplicationException import ApplicationException

class CredentialResolver(object, IConfigurable, IReferenceable):
    _credentials = None
    _references = None

    def __init__(self, config = None, references = None):
        self._credentials = []
        if config != None:
            self.configure(config)
        if references != None:
            self.set_references(references)

    def set_references(self, references):
        self._references = references

    def configure(self, config):
        credentials = CredentialParams.many_from_config(config)
        for credential in credentials:
            self._credentials.append(credential)

    def get_all(self):
        return list(self._credentials)

    def add(self, connection):
        self._credentials.append(connection);

    def _lookup_in_stores(self, correlation_id, credential):
        if credential.use_credential_store() == False: return None
        
        key = credential.get_store_key()
        if self._references == None:
            return None
        
        descriptor = Descriptor("*", "credential_store", "*", "*", "*")
        components = self._references.get_optional(descriptor)
        if len(components) == 0:
            raise ReferenceException(correlation_id, "Credential store wasn't found to make lookup")

        for component in components:
            if isinstance(component, ICredentialStore):
                resolved_credential = component.lookup(correlation_id, key)
                if resolved_credential != None:
                    return resolved_credential

        return None

    def lookup(self, correlation_id):
        if len(self._credentials) == 0: return None
        
        # Return connection that doesn't require discovery
        for credential in self._credentials:
            if not credential.use_credential_store():
                return credential
        
        # Return connection that require discovery
        for credential in self._credentials:
            if credential.use_credential_store():
                resolved_connection = self._lookup_in_stores(correlation_id, credential)
                if resolved_connection != None:
                    return resolved_connection
        
        return None

