# -*- coding: utf-8 -*-
"""
    pip_services_container.info.ContainerInfo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container info implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

from pip_services_commons.data import StringValueMap
from pip_services_commons.data import IdGenerator
from pip_services_commons.config import ConfigParams
from pip_services_commons.config import IReconfigurable

class ContainerInfo(object, IReconfigurable):
    name = None
    description = None
    container_id = None
    start_time = None
    properties = None

    def __init__(self, name = None, description = None):
        self.name = name if name != None else "unknown"
        self.description = description
        self.start_time = datetime.datetime.utcnow()
        self.container_id = IdGenerator.next_long()


    def configure(self, config):
        self.name = config.get_as_string_with_default("name", self.name)
        self.name = config.get_as_string_with_default("info.name", self.name)

        self.description = config.get_as_string_with_default("description", self.description)
        self.description = config.get_as_string_with_default("info.description", self.description)

        self.properties = config.get_section("properties")


    def uptime():
        current_time = datetime.datetime.utcnow()
        return current_time - start_time


    @staticmethod
    def from_config(config):
        result = ContainerInfo()
        result.configure(config)
        return result

