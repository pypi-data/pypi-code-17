# -*- coding: utf-8 -*-
"""
    pip_services_commons.counters.LogCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log counters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .CachedCounters import CachedCounters
from .CounterType import CounterType
from ..log.CompositeLogger import CompositeLogger
from ..convert.StringConverter import StringConverter
from ..refer.IReferenceable import IReferenceable

class LogCounters(CachedCounters, IReferenceable):
    _logger = None

    def __init__(self):
        super(LogCounters, self).__init__()
        self._logger = CompositeLogger() 


    def get_descriptor(self):
        return LogCountersDescriptor


    def set_references(self, references):
        self._logger.set_references(references)


    def _counter_to_string(self, counter):
        result = "Counter " + counter.name + " { "
        result += "\"type\": " + str(counter.type)
        if counter.last != None:
            result += ", \"last\": " + StringConverter.to_string(counter.last)
        if counter.count != None:
            result += ", \"count\": " + StringConverter.to_string(counter.count)
        if counter.min != None:
            result += ", \"min\": " + StringConverter.to_string(counter.min)
        if counter.max != None:
            result += ", \"max\": " + StringConverter.to_string(counter.max)
        if counter.average != None:
            result += ", \"avg\": " + StringConverter.to_string(counter.average)
        if counter.time != None:
            result += ", \"time\": " + StringConverter.to_string(counter.time)
        result += " }"
        return result

    @staticmethod
    def _get_counter_name(counter):
        return counter.name

    def _save(self, counters):
        if self._logger == None:
            return
        if len(counters) == 0:
            return

        # Sort counters by name
        counters = sorted(counters, key=LogCounters._get_counter_name)

        for counter in counters:
            self._logger.info("counters", self._counter_to_string(counter))
