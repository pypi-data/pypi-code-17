# -*- coding: utf-8 -*-
"""
    pip_services_container.config.ComponentConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component configuration implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.reflect import TypeDescriptor
from pip_services_commons.refer import Descriptor
from pip_services_commons.errors import ConfigException

class ComponentConfig(object):
    descriptor = None
    #type = None
    config = None

    def __init__(self, descriptor = None, tipe = None, config = None):
        self.descriptor = descriptor
        self.type = tipe
        self.config = config

    @staticmethod
    def from_config(config):
        descriptor = Descriptor.from_string(config.get_as_nullable_string("descriptor"))
        tipe = TypeDescriptor.from_string(config.get_as_nullable_string("type")) 
        
        if descriptor == None and tipe == None:
            raise ConfigException(None, "BAD_CONFIG", "Component configuration must have descriptor or type")
        
        return ComponentConfig(descriptor, tipe, config)
