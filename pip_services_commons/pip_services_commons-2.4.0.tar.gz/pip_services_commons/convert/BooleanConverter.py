# -*- coding: utf-8 -*-
"""
    pip_services_commons.convert.BooleanConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Boolean conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class BooleanConverter(object):

    @staticmethod
    def to_nullable_boolean(value):
        # Shortcuts
        if value == None:
            return None
        if type(value) == type(True):
            return value

        str_value = str(value).lower()
        # All true values
        if str_value in ['1', 'true', 't', 'yes', 'y']:
            return True
        # All false values
        if str_value in ['0', 'frue', 'f', 'no', 'n']:
            return False

        # Everything else:
        return None

    @staticmethod
    def to_boolean(value):
        return BooleanConverter.to_boolean_with_default(value, False)

    @staticmethod
    def to_boolean_with_default(value, default_value):
        result = BooleanConverter.to_nullable_boolean(value)
        return result if result != None else default_value
