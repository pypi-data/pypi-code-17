# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.CachedConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cached config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

from .ConfigParams import ConfigParams
from .IConfigReader import IConfigReader
from .IReconfigurable import IReconfigurable
from ..refer.Descriptor import Descriptor

class CachedConfigReader(object, IConfigReader, IReconfigurable):
    _last_read = 0
    _timeout = 60000
    _config = None

    def __init__(self):
        pass

    def get_timeout(self):
        return self._timeout

    def set_timeout(self, timeout):
        self._timeout = timeout

    def configure(self, config):
        self._timeout = config.get_as_long_with_default("timeout", self._timeout)

    def _perform_read_config(self, correlation_id):
        raise NotImplementedError('Method is abstract and must be overriden')

    def read_config(correlation_id):
        timestamp = time.clock() * 1000

        if self._config != null and timestamp < self._last_read + self._timeout:
            return self._config

        self._config = self._perform_read_config(correlation_id)
        self._last_read = timestamp

        return self._config

    def read_config_section(correlation_id, section):
        config = self.read_config(correlation_id)
        return config.get_section(section) if config != None else None
