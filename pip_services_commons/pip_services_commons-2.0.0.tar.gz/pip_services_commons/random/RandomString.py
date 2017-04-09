# -*- coding: utf-8 -*-
"""
    pip_services_commons.random.RandomString
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomString implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

from .RandomInteger import RandomInteger
from .RandomBoolean import RandomBoolean 

_digits = "01234956789"
_symbols = "_,.:-/.[].{},#-!,$=%.+^.&*-() "
_alpha_lower = "abcdefghijklmnopqrstuvwxyz"
_alpha_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
_alpha = _alpha_upper + _alpha_lower
_chars = _alpha + _digits + _symbols

class RandomString(object):

    @staticmethod
    def pick(values):
        if values == None or len(values) == 0:
            return None

        return random.choice(values)

    @staticmethod
    def distort(value):
        value = value.lower()

        if (RandomBoolean.chance(1, 5)):
            value = value[0:1].upper() + value[1:]

        if (RandomBoolean.chance(1, 3)):
            value = value + random.choice(_symbols)

        return value

    @staticmethod
    def next_alpha_char():
        return random.choice(_alpha)

    @staticmethod
    def next_string(min_size, max_size):
        result = ''
        
        max_size = max_size if max_size != None else min_size
        length = RandomInteger.next_integer(min_size, max_size)
        for i in range(length):
            result += random.choice(_chars)

        return result
