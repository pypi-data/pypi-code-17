# -*- coding: utf-8 -*-
"""
    pip_services_container.Container
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import traceback

from pip_services_commons.config import IConfigurable
from pip_services_commons.log import NullLogger
from pip_services_commons.log import CompositeLogger
from pip_services_commons.errors import InvalidStateException
from pip_services_commons.refer import Descriptor
from pip_services_commons.refer import IReferenceable
from pip_services_commons.refer import IUnreferenceable
from pip_services_commons.refer import Referencer
from pip_services_commons.run import IOpenable
from pip_services_commons.run import Opener
from pip_services_commons.run import Closer

from .build.DefaultContainerFactory import DefaultContainerFactory
from .build.DefaultContainerFactory import DefaultContainerFactoryDescriptor
from .info.ContainerInfo import ContainerInfo
from .info.ContainerInfoFactory import ContainerInfoDescriptor
from .config.ContainerConfigReader import ContainerConfigReader
from .refer.ContainerReferences import ContainerReferences

class Container(object, IConfigurable, IReferenceable, IUnreferenceable, IOpenable):
    _logger = None
    _info = None
    _config = None
    _factories = None
    _references = None

    def __init__(self, name = None, description = None):
        self._logger = NullLogger()
        self._info = ContainerInfo(name, description)
        self._factories = DefaultContainerFactory()

    def configure(self, config):
        self._config = ContainerConfig.from_config(config)

    def read_config_from_file(self, correlation_id, path, parameters):
        self._config = ContainerConfigReader.read_from_file(correlation_id, path, parameters)

    def set_references(self, references):
        pass

    def unset_references(self):
        pass
        
    def _init_references(self, references):
        # Override in base classes
        references.put(DefaultContainerFactoryDescriptor, self._factories)
        references.put(ContainerInfoDescriptor, self._info)

    def is_opened(self):
        return self._references != None

    def open(self, correlation_id):
        if self._references != None:
            raise InvalidStateException(correlation_id, "ALREADY_OPENED", "Container was already opened")
                
        try:
            self._logger.trace(correlation_id, "Starting container.")
            
            # Create references with configured components
            self._references = ContainerReferences()
            self._init_references(self._references)
            self._references.put_from_config(self._config)
            self.set_references(self._references)

            # Get custom description if available
            info_descriptor = Descriptor("*", "container-info", "*", "*", "*")
            self._info = self._references.get_one_optional(info_descriptor)

            # Reference and open components
            self._references.open(correlation_id)

            # Get reference to logger
            self._logger = CompositeLogger(self._references)
            self._logger.info(correlation_id, "Container " + self._info.name + " started.")
        except Exception as ex:
            self._logger.error(correlation_id, ex, "Failed to start container")
            traceback.print_exc()
            raise ex

    def close(self, correlation_id):
        if self._references == None:
            return;
                
        try:
            self._logger.trace(correlation_id, "Stopping " + self._info.name + " container")

            # Unset references for child container
            self.unset_references()

            # Close and deference components
            self._references.close(correlation_id)
            self._references = None

            self._logger.info(correlation_id, "Container " + self._info.name + " stopped")
        except Exception as ex:
            self._logger.error(correlation_id, ex, "Failed to stop container")
            raise ex
