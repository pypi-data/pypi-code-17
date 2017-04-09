# -*- coding: utf-8 -*-
"""
    pip_services_commons.counters.CachedCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cached counters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading
import datetime

from .ICounters import ICounters
from .Counter import Counter
from .CounterType import CounterType
from .ITimingCallback import ITimingCallback
from .Timing import Timing
from ..config.IReconfigurable import IReconfigurable

class CachedCounters(object, ICounters, IReconfigurable, ITimingCallback):
    _default_interval = 300000

    _cache = None
    _updated = None
    _last_dump_time = None
    _interval = None
    _lock = None


    def __init__(self):
        self._cache = {}
        self._updated = False
        self._last_dump_time = time.clock()
        self._interval = self._default_interval
        self._lock = threading.Lock()


    def _save(counters):
        raise NotImplementedError('Method from abstract implementation')


    def configure(self, config):
        self._interval = config.get_as_float_with_default("interval", self._interval)


    def clear(self, name):
        self._lock.acquire()
        try:
            del self._cache[name]
        finally:
            self._lock.release()


    def clear_all(self):
        self._lock.acquire()
        try:
            self._cache = {}
            self._updated = False
        finally:
            self._lock.release()


    def dump(self):
        if self._updated:
            messages = self.get_all()
            self._save(messages)

            self._lock.acquire()
            try:
                self._updated = False
                current_time = time.clock() * 1000
                self._last_dump_time = current_time
            finally:
                self._lock.release()


    def _update(self):
        self._updated = True
        
        current_time = time.clock() * 1000
        if current_time > self._last_dump_time + self._interval:
            try:
                self.dump()
            except:
                # Todo: decide what to do
                pass


    def get_all(self):
        self._lock.acquire()
        try:
            return list(self._cache.values())
        finally:
            self._lock.release()


    def get(self, name, typ):
        if name == None or len(name) == 0:
            raise Exception("Counter name was not set")

        self._lock.acquire()
        try:
            counter = self._cache[name] if name in self._cache else None

            if counter == None or counter.type != typ:
                counter = Counter(name, typ)
                self._cache[name] = counter

            return counter
        finally:
            self._lock.release()


    def _calculate_stats(self, counter, value):
        if counter == None:
            raise Exception("Missing counter")

        counter.last = value
        counter.count = counter.count + 1 if counter.count != None else 1
        counter.max = max(counter.max, value) if counter.max != None else value
        counter.min = min(counter.min, value) if counter.min != None else value
        counter.average = (float(counter.average * (counter.count - 1)) + value) / counter.count \
            if counter.average != None and counter.count > 0 else value


    def begin_timing(self, name):
        return Timing(name, self)


    def end_timing(self, name, elapsed):
        counter = self.get(name, CounterType.Interval)
        self._calculate_stats(counter, elapsed)
        self._update()


    def stats(self, name, value):
        counter = self.get(name, CounterType.Statistics)
        self._calculate_stats(counter, value)
        self._update()


    def last(self, name, value):
        counter = self.get(name, CounterType.LastValue)
        counter.last = value
        self._update()


    def timestamp_now(self, name):
        self.timestamp(name, datetime.datetime.utcnow())


    def timestamp(self, name, value):
        counter = self.get(name, CounterType.Timestamp)
        counter.time = value if value != None else datetime.datetime.utcnow()
        self._update()


    def increment_one(self, name):
        self.increment(name, 1)


    def increment(self, name, value):
        counter = self.get(name, CounterType.Increment)
        counter.count = counter.count + value if counter.count != None else value
        self._update()
