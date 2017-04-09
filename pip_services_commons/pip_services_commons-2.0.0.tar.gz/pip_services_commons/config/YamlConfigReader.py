# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.YamlConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    YAML config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import os.path
import yaml 

from ..errors.FileException import FileException
from ..errors.ConfigException import ConfigException
from .ConfigParams import ConfigParams
from .FileConfigReader import FileConfigReader

class YamlConfigReader(FileConfigReader):

    def __init__(self, path):
        super(YamlConfigReader, self).__init__(path)
    
    def _read_object(self, correlation_id):
        path = self.get_path()

        if path == None:
            raise ConfigException(correlation_id, "NO_PATH", "Missing config file path")
        
        if not os.path.isfile(path):
            raise FileException(correlation_id, 'FILE_NOT_FOUND', 'Config file was not found at ' + path)
        
        try:
            with open(path, 'r') as file:
                return yaml.load(file)
        except Exception as ex:
            raise FileException(
                correlation_id,
                "READ_FAILED",
                "Failed reading configuration " + path + ": " + str(ex)
            ).with_details("path", path).with_cause(ex)

    def _perform_read_config(correlation_id):
        value = self._read_object(correlation_id)
        return ConfigParams.from_value(value)

    @staticmethod
    def read_object(correlation_id, path):
        return YamlConfigReader(path)._read_object(correlation_id)

    @staticmethod
    def read_config(correlation_id, path):
        value = YamlConfigReader(path)._read_object(correlation_id)
        return ConfigParams.from_value(value)