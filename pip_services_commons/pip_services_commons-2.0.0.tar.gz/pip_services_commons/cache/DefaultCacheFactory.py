# -*- coding: utf-8 -*-
"""
    pip_services_commons.cache.DefaultCacheFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default cache factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .NullCache import NullCache
from .MemoryCache import MemoryCache

from ..refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultCacheFactoryDescriptor = Descriptor(
    "pip-services-commons", "factory", "cache", "default", "1.0"
)

NullCacheDescriptor = Descriptor(
    "pip-services-commons", "cache", "null", "*", "1.0"
)

MemoryCacheDescriptor = Descriptor(
    "pip-services-commons", "cache", "memory", "*", "1.0"
)

class DefaultCacheFactory(Factory):

    def __init__(self):
        self.register_as_type(NullCacheDescriptor, NullCache)
        self.register_as_type(MemoryCacheDescriptor, MemoryCache)
