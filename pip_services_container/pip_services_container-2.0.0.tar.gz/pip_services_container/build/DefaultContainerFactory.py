# -*- coding: utf-8 -*-
"""
    pip_services_container.build.DefaultContainerFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default container factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.refer import Descriptor
from pip_services_commons.build import CompositeFactory
from pip_services_commons.log import DefaultLoggerFactory
from pip_services_commons.count import DefaultCountersFactory
from pip_services_commons.config import DefaultConfigReaderFactory
from pip_services_commons.cache import DefaultCacheFactory
from pip_services_commons.auth import DefaultCredentialStoreFactory
from pip_services_commons.connect import DefaultDiscoveryFactory
from ..info.ContainerInfoFactory import ContainerInfoFactory

DefaultContainerFactoryDescriptor = Descriptor(
    "pip-services-container", "factory", "container", "default", "1.0"
)

class DefaultContainerFactory(CompositeFactory):

    def __init__(self):
        super(DefaultContainerFactory, self).__init__()
        self.add(ContainerInfoFactory())
        self.add(DefaultLoggerFactory())
        self.add(DefaultCountersFactory())
        self.add(DefaultConfigReaderFactory())
        self.add(DefaultCacheFactory())
        self.add(DefaultCredentialStoreFactory())
        self.add(DefaultDiscoveryFactory())

