# -*- coding: utf-8 -*-
"""
    pip_services_container.config.ContainerConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container configuration implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.config import ConfigParams
from .ComponentConfig import ComponentConfig

class ContainerConfig(list):

    def __init__(self, components = None):
        if components != None:
            for component in components:
                self.append(component)

    @staticmethod
    def from_value(value):
        config = ConfigParams.from_value(value)
        return from_config(config)

    @staticmethod
    def from_config(config):
        result = ContainerConfig()
        if config == None:
            return result
        
        for section in config.get_section_names():
            component_config = config.get_section(section)
            result.append(ComponentConfig.from_config(component_config))
        
        return result
