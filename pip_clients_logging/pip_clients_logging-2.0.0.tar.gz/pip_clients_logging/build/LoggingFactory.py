# -*- coding: utf-8 -*-
"""
    pip_clients_logging.build.LoggingFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..log.DirectLogger import DirectLogger
from ..log.HttpLogger import HttpLogger

from ..version1.LoggingNullClientV1 import LoggingNullClientV1
from ..version1.LoggingDirectClientV1 import LoggingDirectClientV1
from ..version1.LoggingHttpClientV1 import LoggingHttpClientV1

from pip_services_commons.refer import Descriptor
from pip_services_commons.build import Factory

LoggingFactoryDescriptor = Descriptor(
    "pip-services-logging", "factory", "client", "default", "1.0"
)

DirectLoggerDescriptor = Descriptor(
    "pip-services-logging", "logger", "direct", "*", "1.0"
)

HttpLoggerDescriptor = Descriptor(
    "pip-services-logging", "logger", "http", "*", "1.0"
)

LoggingNullClientV2Descriptor = Descriptor(
    "pip-services-logging", "client", "null", "*", "1.0"
)

LoggingDirectClientV2Descriptor = Descriptor(
    "pip-services-logging", "direct", "direct", "*", "1.0"
)

LoggingHttpClientV2Descriptor = Descriptor(
    "pip-services-logging", "http", "direct", "*", "1.0"
)

class LoggingFactory(Factory):

    def __init__(self):
        self.register_as_type(DirectLoggerDescriptor, DirectLogger)
        self.register_as_type(HttpLoggerDescriptor, HttpLogger)
        self.register_as_type(LoggingNullClientV1Descriptor, LoggingNullClientV1)
        self.register_as_type(LoggingDirectClientV1Descriptor, LoggingDirectClientV1)
        self.register_as_type(LoggingHttpClientV1Descriptor, LoggingHttpClientV1)

