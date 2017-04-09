# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.CompositeCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Composite counters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICounters import ICounters
from .ITimingCallback import ITimingCallback
from .Timing import Timing
from ..refer.Descriptor import Descriptor
from ..refer.IReferenceable import IReferenceable

class CompositeCounters(ICounters, ITimingCallback, IReferenceable):
    _counters = None

    def __init__(self, references = None):
        self._counters = []

        if references != None:
            self.set_references(references)
            
    def set_references(self, references):
        descriptor = Descriptor(None, "counters", None, None, None)
        counters = references.get_optional(descriptor)
        for counter in counters:
            if isinstance(counter, ICounters):
                self._counters.append(counter)

    def begin_timing(self, name):
        return Timing(name, self)

    def end_timing(self, name, elapsed):
        for counter in self._counters:
            if isinstance(counter, ITimingCallback):
                counter.end_timing(name, elapsed)

    def stats(self, name, value):
        for counter in self._counters:
            counter.stats(name, value)

    def last(self, name, value):
        for counter in self._counters:
            counter.last(name, value)

    def timestamp_now(self, name):
        for counter in self._counters:
            counter.timestamp_now(name)

    def timestamp(self, name, value):
        for counter in self._counters:
            counter.timestamp(name, value)

    def increment_one(self, name):
        for counter in self._counters:
            counter.increment_one(name)

    def increment(self, name, value):
        for counter in self._counters:
            counter.increment(name, value)
