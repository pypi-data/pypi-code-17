# -*- coding: utf-8 -*-
"""
    pip_services_commons.auth.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Authentication module initialization
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [ 'CredentialParams', 'ICredentialStore', 'CredentialResolver',
    'MemoryCredentialStore', 'DefaultCredentialStoreFactory' ]

from .CredentialParams import CredentialParams
from .ICredentialStore import ICredentialStore
from .CredentialResolver import CredentialResolver
from .MemoryCredentialStore import MemoryCredentialStore
from .DefaultCredentialStoreFactory import DefaultCredentialStoreFactory

