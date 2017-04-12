# -*- coding: utf-8 -*-
"""
    pip_services_container.config.ContainerConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container configuration reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.errors import ConfigException
from pip_services_commons.config import JsonConfigReader
from pip_services_commons.config import YamlConfigReader
from .ContainerConfig import ContainerConfig

class ContainerConfigReader(object):

    @staticmethod
    def read_from_file(correlation_id, path, parameters):
        if path == None:
            raise ConfigException(correlation_id, "NO_PATH", "Missing config file path")
        
        index = path.rfind('.')
        ext = path[index + 1:].lower() if index > 0 else ''

        if ext == "json":
            return ContainerConfigReader.read_from_json_file(correlation_id, path, parameters)
        elif ext == "yaml":
            return ContainerConfigReader.read_from_yaml_file(correlation_id, path, parameters)
        
        # By default read as JSON
        return ContainerConfigReader.read_from_json_file(correlation_id, path, parameters)

    @staticmethod
    def read_from_json_file(correlation_id, path, parameters):
        config = JsonConfigReader.read_config(correlation_id, path, parameters)
        return ContainerConfig.from_config(config)

    @staticmethod
    def read_from_yaml_file(correlation_id, path, parameters):
        config = YamlConfigReader.read_config(correlation_id, path, parameters)
        return ContainerConfig.from_config(config)

