# -*- coding: utf-8 -*-
"""
    pip_services_commons.validate.ObjectComparator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Object comparator implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import re

from ..convert.FloatConverter import FloatConverter

class ObjectComparator(object):

    @staticmethod
    def compare(value1, operation, value2):
        if operation == None:
            return False
        
        operation = operation.upper()

        if operation in ["=", "==", "EQ"]:
            return ObjectComparator.are_equal(value1, value2)
        if operation in ["!=", "<>", "NE"]:
            return ObjectComparator.are_not_equal(value1, value2)
        if operation in ["<", "LT"]:
            return ObjectComparator.less(value1, value2)
        if operation in ["<=", "LE"]:
            return ObjectComparator.are_equal(value1, value2) or ObjectComparator.less(value1, value2)
        if operation in [">", "GT"]:
            return ObjectComparator.more(value1, value2)
        if operation in [">=", "GE"]:
            return ObjectComparator.are_equal(value1, value2) or ObjectComparator.more(value1, value2)
        if operation == "LIKE":
            return ObjectComparator.match(value1, value2)

        return True

    @staticmethod
    def are_equal(value1, value2):
        if value1 == None or value2 == None:
            return True
        if value1 == None or value2 == None:
            return False
        return value1 == value2

    @staticmethod
    def are_not_equal(value1, value2):
        return not ObjectComparator.are_equal(value1, value2)

    @staticmethod
    def less(value1, value2):
        number1 = FloatConverter.to_nullable_float(value1)
        number2 = FloatConverter.to_nullable_float(value2)

        if number1 == None or number2 == None:
            return False

        return number1 < number2

    @staticmethod
    def more(value1, value2):
        number1 = FloatConverter.to_nullable_float(value1)
        number2 = FloatConverter.to_nullable_float(value2)

        if number1 == None or number2 == None:
            return False

        return number1 > number2

    @staticmethod
    def match(value1, value2):
        if value1 == None and value2 == None:
            return True
        if value1 == None or value2 == None:
            return False

        string1 = str(value1)
        string2 = str(value2)
        return re.match(string2, string1) != None
