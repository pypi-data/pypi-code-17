# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.DateTimeConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    DateTime conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from datetime import *
import iso8601
from .UTC import UTC

class DateTimeConverter(object):

    @staticmethod
    def to_nullable_datetime(value):
        # Shortcuts
        if value == None:
            return None
        if type(value) == datetime:
            return DateTimeConverter.to_utc_datetime(value) 

        if type(value) in (int, float, long):
            value = datetime.fromtimestamp(value)
            return DateTimeConverter.to_utc_datetime(value) 
        if type(value) == date:
            value = datetime.combine(value, time(0,0,0))
            return DateTimeConverter.to_utc_datetime(value) 
        if type(value) == time:
            value = datetime.combine(datetime.utcnow().date, value)
            return DateTimeConverter.to_utc_datetime(value) 
        
        try:
            value = str(value)
            value = iso8601.parse_date(value)
            return DateTimeConverter.to_utc_datetime(value) 
        except:
            return None

    @staticmethod
    def to_datetime(value):
        return DateTimeConverter.to_datetime_with_default(value, None)

    @staticmethod
    def to_datetime_with_default(value, default_value):
        result = DateTimeConverter.to_nullable_datetime(value)
        return result if result != None else DateTimeConverter.to_utc_datetime(default_value)

    @staticmethod
    def to_utc_datetime(value):
        if value == None:
            return value
        elif type(value) == datetime:
            if value.tzinfo == None:
                value = value.replace(tzinfo=UTC)
            return value
        else:
            return DateTimeConverter.to_nullable_datetime(value)
