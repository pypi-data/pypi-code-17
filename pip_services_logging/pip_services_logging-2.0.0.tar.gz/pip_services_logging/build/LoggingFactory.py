# -*- coding: utf-8 -*-
"""
    pip_services_logging.build.LoggingFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..persistence.LoggingMemoryPersistence import LoggingMemoryPersistence
from ..logic.LoggingController import LoggingController
from ..services.version1.LoggingHttpServiceV1 import LoggingHttpServiceV1

from pip_services_commons.refer import Descriptor
from pip_services_commons.build import Factory

LoggingFactoryDescriptor = Descriptor(
    "pip-services-logging", "factory", "service", "default", "1.0"
)

LoggingMemoryPersistenceDescriptor = Descriptor(
    "pip-services-logging", "persistence", "memory", "*", "1.0"
)

LoggingControllerDescriptor = Descriptor(
    "pip-services-logging", "controller", "default", "*", "1.0"
)

LoggingHttpServiceV1Descriptor = Descriptor(
    "pip-services-logging", "service", "http", "*", "1.0"
)

class LoggingFactory(Factory):

    def __init__(self):
        self.register_as_type(LoggingMemoryPersistenceDescriptor, LoggingMemoryPersistence)
        self.register_as_type(LoggingControllerDescriptor, LoggingController)
        self.register_as_type(LoggingHttpServiceV1Descriptor, LoggingHttpServiceV1)

