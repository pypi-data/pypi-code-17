# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.DefaultLoggerFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default logger factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .NullLogger import NullLogger
from .ConsoleLogger import ConsoleLogger
from .CompositeLogger import CompositeLogger

from ..refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultLoggerFactoryDescriptor = Descriptor(
    "pip-services-commons", "factory", "logger", "default", "1.0"
)

NullLoggerDescriptor = Descriptor(
    "pip-services-commons", "logger", "null", "*", "1.0"
)

ConsoleLoggerDescriptor = Descriptor(
    "pip-services-commons", "logger", "console", "*", "1.0"
)

CompositeLoggerDescriptor = Descriptor(
    "pip-services-commons", "logger", "composite", "*", "1.0"
)

class DefaultLoggerFactory(Factory):

    def __init__(self):
        self.register_as_type(NullLoggerDescriptor, NullLogger)
        self.register_as_type(ConsoleLoggerDescriptor, ConsoleLogger)
        self.register_as_type(CompositeLoggerDescriptor, CompositeLogger)
