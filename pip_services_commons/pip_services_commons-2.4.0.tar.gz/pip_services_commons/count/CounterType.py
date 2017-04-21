# -*- coding: utf-8 -*-
"""
    pip_services_commons.counters.CounterType
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Counter type enumeration
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class CounterType(object):
    Interval = 0
    LastValue = 1
    Statistics = 2
    Timestamp = 3
    Increment = 4

    @staticmethod
    def to_string(typ):
        if typ == CounterType.Interval:
            return "INTERVAL" 
        if typ == CounterType.LastValue:
            return "LAST" 
        if typ == CounterType.Statistics:
            return "STATS" 
        if typ == CounterType.Timestamp:
            return "TIME"
        if typ == CounterType.Increment:
            return "COUNT"
        return "UNDEF"
