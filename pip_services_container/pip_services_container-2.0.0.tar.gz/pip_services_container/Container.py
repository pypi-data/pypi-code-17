# -*- coding: utf-8 -*-
"""
    pip_services_container.Container
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import traceback

from pip_services_commons.log import NullLogger
from pip_services_commons.log import CompositeLogger
from pip_services_commons.errors import InvalidStateException
from pip_services_commons.refer import Descriptor
from pip_services_commons.run import Opener
from pip_services_commons.run import Closer
from pip_services_commons.refer import Referencer

from .build.DefaultContainerFactory import DefaultContainerFactory
from .build.DefaultContainerFactory import DefaultContainerFactoryDescriptor
from .info.ContainerInfo import ContainerInfo
from .config.ContainerConfigReader import ContainerConfigReader
from .refer.ContainerReferences import ContainerReferences

class Container(object):
    _logger = None
    _info = None
    _config = None
    _references = None

    def __init__(self, config = None):
        self._logger = NullLogger()
        self._info = ContainerInfo()
        self._references = ContainerReferences()
        self._config = config

    def get_info(self):
        return self._info

    def set_info(self, info):
        self._info = info

    def get_config(self):
        return self._config

    def set_config(self, value):
        self._config = value

    def get_references(self):
        return self._references

    def set_references(self, references):
        self._references = references

    def read_config_from_file(self, correlation_id, path):
        self._config = ContainerConfigReader.read_from_file(correlation_id, path)
        
    def _init_references(self, references):
        # Override in base classes
        references.put(DefaultContainerFactoryDescriptor, DefaultContainerFactory())

    def start(self, correlation_id):
        if self._references == None:
            raise InvalidStateException(correlation_id, "NO_CONFIG", "Container was not configured")
                
        try:
            self._logger.trace(correlation_id, "Starting container.")
            
            # Create references with configured components
            self._init_references(self._references)
            self._references.put_from_config(self._config)

            # Reference and open components
            components = self._references.get_all()
            Referencer.set_references(self._references, components)
            Opener.open(correlation_id, components)

            # Get reference to logger
            self._logger = CompositeLogger(self._references)
            
            # Get reference to container info
            info_descriptor = Descriptor("*", "container-info", "*", "*", "*")
            self._info = self._references.get_one_required(info_descriptor)
            self._logger.info(correlation_id, "Container " + self._info.name + " started.")
        except Exception as ex:
            self._references = None
            self._logger.error(correlation_id, ex, "Failed to start container")
            traceback.print_exc()
            raise ex

    def stop(self, correlation_id):
        if self._references == None:
            raise InvalidStateException(correlation_id, "NO_STARTED", "Container was not started")
                
        try:
            self._logger.trace(correlation_id, "Stopping " + self._info.name + " container")

            # Close and deference components
            self._references.close(correlation_id)

            self._logger.info(correlation_id, "Container " + self._info.name + " stopped")
        except Exception as ex:
            self._logger.error(correlation_id, ex, "Failed to stop container")
            raise ex
