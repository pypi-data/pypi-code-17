# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.StringConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    String conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

class StringConverter(object):

    @staticmethod
    def to_nullable_string(value):
        if value == None:
            return None
        if type(value) == datetime.date:
            return value.isoformat()
        if type(value) == datetime.datetime:
            if value.tzinfo == None:
                return value.isoformat() + "Z"
            else:
                return value.isoformat()
        return str(value)

    @staticmethod
    def to_string(value):
        return StringConverter.to_string_with_default(value, None)

    @staticmethod
    def to_string_with_default(value, default_value):
        result = StringConverter.to_nullable_string(value)
        return result if result != None else default_value
