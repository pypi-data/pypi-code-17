# -*- coding: utf-8 -*-
"""
    pip_services_common.auth.ICredentialStore
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Credential store interface
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .CredentialParams import CredentialParams

class ICredentialStore:
    """
    Store that keeps and located client credentials.
    """

    def store(self, correlation_id, key, credential):
        """
        Stores credential in the store

        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: the key to lookup credential
            credential: a credential parameters
        """
        raise NotImplementedError('Method from interface definition')

    def lookup(self, correlation_id, key):
        """
        Looks up credential from the store

        Args:
            correlation_id: a unique transaction id to trace calls across components
            key: a key to lookup credential

        Returns: found credential parameters or None if nothing was found
        """
        raise NotImplementedError('Method from interface definition')