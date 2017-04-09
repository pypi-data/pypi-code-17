# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.IntegerConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Integer conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IntegerConverter(object):
    
    @staticmethod
    def to_nullable_integer(value):
        # Shortcuts
        if value == None:
            return None

        try:
            value = float(value)
            return int(value)
        except:
            return None

    @staticmethod
    def to_integer(value):
        return IntegerConverter.to_integer_with_default(value, 0)

    @staticmethod
    def to_integer_with_default(value, default_value):
        result = IntegerConverter.to_nullable_integer(value)
        return result if result != None else default_value
