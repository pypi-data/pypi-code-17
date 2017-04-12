# -*- coding: utf-8 -*-
"""
    pip_services_commons.connect.DefaultConfigReaderFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default discovery factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .MemoryConfigReader import MemoryConfigReader
from .JsonConfigReader import JsonConfigReader
from .YamlConfigReader import YamlConfigReader

from ..refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultDiscoveryFactoryDescriptor = Descriptor(
    "pip-services-commons", "factory", "config-reader", "default", "1.0"
)

MemoryConfigReaderDescriptor = Descriptor(
    "pip-services-commons", "config-reader", "memory", "*", "1.0"
)

JsonConfigReaderDescriptor = Descriptor(
    "pip-services-commons", "config-reader", "json", "*", "1.0"
)

YamlConfigReaderDescriptor = Descriptor(
    "pip-services-commons", "config-reader", "yaml", "*", "1.0"
)

class DefaultConfigReaderFactory(Factory):

    def __init__(self):
        self.register_as_type(MemoryConfigReaderDescriptor, MemoryConfigReader)
        self.register_as_type(JsonConfigReaderDescriptor, JsonConfigReader)
        self.register_as_type(YamlConfigReaderDescriptor, YamlConfigReader)
