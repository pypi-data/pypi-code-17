# -*- coding: utf-8 -*-
"""
    pip_services_data.file.JsonFilePersister
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    JSON file persister implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import json
import os

from pip_services_commons.config import IConfigurable
from pip_services_commons.errors import ConfigException, FileException

from ..ILoader import ILoader
from ..ISaver import ISaver

class JsonFilePersister(object, ILoader, ISaver, IConfigurable):
    path = None

    def __init__(self, path = None):
        self.path = path

    def configure(self, config):
        if config == None or not config.contains_key("path"):
            raise ConfigException(None, "NO_PATH", "Data file path is not set")

        self.path = config.get_as_string("path")

    def load(self, correlation_id):
        # If doesn't exist then consider empty data
        if not os.path.isfile(self.path):
            return []

        try:
            with open(self.path, 'r') as file:
                return json.load(file)
        except Exception as ex:
            raise FileException(correlation_id, "READ_FAILED", "Failed to read data file: " + str(ex)) \
                .with_cause(ex)

    def save(self, correlation_id, entities):
        try:
            with open(self.path, 'w') as file:
                json.dump(entities, file)
        except Exception as ex:
            raise FileException(correlation_id, "WRITE_FAILED", "Failed to write data file: " + str(ex)) \
                .with_cause(ex)
