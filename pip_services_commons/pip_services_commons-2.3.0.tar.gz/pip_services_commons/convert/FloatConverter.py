# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.FloatConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Float conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class FloatConverter(object):

    @staticmethod
    def to_nullable_float(value):
        # Shortcuts
        if value == None:
            return None

        try:
            return float(value)
        except:
            return None

    @staticmethod
    def to_float(value):
        return FloatConverter.to_float_with_default(value, 0.0)

    @staticmethod
    def to_float_with_default(value, default_value):
        result = FloatConverter.to_nullable_float(value)
        return result if result != None else default_value
