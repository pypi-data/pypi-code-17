# -*- coding: utf-8 -*-
"""
    pip_services_commons.count.DefaultCountersFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default counters factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .NullCounters import NullCounters
from .LogCounters import LogCounters
from .CompositeCounters import CompositeCounters

from ..refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultCountersFactoryDescriptor = Descriptor(
    "pip-services-commons", "factory", "counters", "default", "1.0"
)

NullCountersDescriptor = Descriptor(
    "pip-services-commons", "counters", "null", "*", "1.0"
)

LogCountersDescriptor = Descriptor(
    "pip-services-commons", "counters", "log", "*", "1.0"
)

CompositeCountersDescriptor = Descriptor(
    "pip-services-commons", "counters", "composite", "*", "1.0"
)

class DefaultCountersFactory(Factory):

    def __init__(self):
        self.register_as_type(NullCountersDescriptor, NullCounters)
        self.register_as_type(LogCountersDescriptor, LogCounters)
        self.register_as_type(CompositeCountersDescriptor, CompositeCounters)
