# -*- coding: utf-8 -*-
"""
    pip_services_commons.random.RandomDateTime
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomDateTime implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import datetime
import time
import pytz

from .RandomInteger import RandomInteger

class RandomDateTime(object):

    @staticmethod
    def next_date(min_year = None, max_year = None):
        current_year = datetime.datetime.utcnow().year
        min_year = min_year if min_year != None else current_year - RandomInteger.next_integer(10)
        max_year = max_year if max_year != None else current_year

        year = RandomInteger.next_integer(min_year, max_year)
        month = RandomInteger.next_integer(1, 13)
        day = RandomInteger.next_integer(1, 32)
        
        if month == 2:
            day = min(28, day)
        elif month in [4, 6, 9, 11]:
            day = min(30, day)

        return datetime.datetime(year, month, day, 0, 0, 0, 0, pytz.utc)

    @staticmethod
    def next_time():
        hour = RandomInteger.next_integer(0, 24)
        min = RandomInteger.next_integer(0, 60)
        sec = RandomInteger.next_integer(0, 60)
        millis = RandomInteger.next_integer(0, 1000)

        return datetime.time(hour, min, sec, millis)

    @staticmethod
    def next_datetime(min_year = None, max_year = None):
        date = RandomDateTime.next_date(min_year, max_year).date()
        time = RandomDateTime.next_time()
        return datetime.datetime.combine(date, time)

    @staticmethod
    def update_datetime(value, range = None):
        range = range if range != None else 10
        if range < 0:
            return value
        
        days = RandomFloat.next_float(-range, range)

        return value + datetime.timedelta(days)
