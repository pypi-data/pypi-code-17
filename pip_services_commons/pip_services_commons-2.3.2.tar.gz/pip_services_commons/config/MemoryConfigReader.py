# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.MemoryConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConfigParams import ConfigParams
from .IConfigReader import IConfigReader
from .IReconfigurable import IReconfigurable

class MemoryConfigReader(object, IConfigReader, IReconfigurable):
    _config = None

    def __init__(self, config = None):
        self._config = config
        
    def configure(self, config):
        self._config = config

    def read_config(self, correlation_id):
        return ConfigParams(self._config)

    def read_config_section(self, section):
        config = self._config.get_section(section) if self._config != None else None
        return config
