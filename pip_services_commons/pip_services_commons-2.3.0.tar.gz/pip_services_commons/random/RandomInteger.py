# -*- coding: utf-8 -*-
"""
    pip_services_commons.random.RandomInteger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Random integer implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

class RandomInteger(object):

    @staticmethod
    def next_integer(min, max = None):
        if max == None:
            max = min
            min = 0

        if max - min <= 0:
            return min

        return random.randint(min, max - 1)

    @staticmethod
    def update_integer(value, range = None):
        if range == None:
            range = int(0.1 * value)
        
        min = value - range
        max = value + range
        return RandomInteger.next_integer(min, max)

    @staticmethod
    def sequence(min, max = None):
        max = max if max != None else min
        count = RandomInteger.next_integer(min, max)
        return range(count)
