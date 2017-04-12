# -*- coding: utf-8 -*-
"""
    pip_services_commons.config.CachedConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cached config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import pystache

from .ConfigParams import ConfigParams
from .IConfigReader import IConfigReader
from .IReconfigurable import IReconfigurable

class ConfigReader(object, IConfigReader, IReconfigurable):
    _parameters = None

    def __init__(self):
        self._parameters = ConfigParams()

    def configure(self, config):
        parameters = config.get_section("parameters")
        if len(parameters) > 0:
            self._parameters = parameters

    def read_config(self, correlation_id, parameters):
        raise NotImplementedError('Method is abstract and must be overriden')

    def _parameterize(self, config, parameters):
        parameters = self._parameters.override(parameters)
        return pystache.render(config, parameters)
