# -*- coding: utf-8 -*-
"""
    pip_services_commons.count.NullCounter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null counter implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICounters import ICounters
from .Timing import Timing

class NullCounters(object, ICounters):

    def begin_timing(self, name):
        return Timing()

    def stats(self, name, value):
        pass

    def last(self, name, value):
        pass

    def timestamp_now(self, name):
        pass

    def timestamp(self, name, value):
        pass

    def increment_one(self, name):
        pass

    def increment(self, name, value):
        pass
