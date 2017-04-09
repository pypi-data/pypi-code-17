# -*- coding: utf-8 -*-
"""
    pip_services_commons.auth.DefaultCredentialStoreFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default credential store factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .MemoryCredentialStore import MemoryCredentialStore

from ..refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultCredentialStoreFactoryDescriptor = Descriptor(
    "pip-services-commons", "factory", "credential-store", "default", "1.0"
)

MemoryCredentialStoreDescriptor = Descriptor(
    "pip-services-commons", "credential-store", "memory", "*", "1.0"
)

class DefaultCredentialStoreFactory(Factory):

    def __init__(self):
        self.register_as_type(MemoryCredentialStoreDescriptor, MemoryCredentialStore)
