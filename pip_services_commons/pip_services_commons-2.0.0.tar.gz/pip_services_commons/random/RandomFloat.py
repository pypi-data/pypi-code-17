# -*- coding: utf-8 -*-
"""
    pip_services_commons.random.RandomFloat
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomFloat implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

class RandomFloat(object):

    @staticmethod
    def next_float(min, max = None):
        if max == None:
            max = min
            min = 0

        if max - min <= 0:
            return min

        return min + random.random() * (max - min)

    @staticmethod
    def update_float(value, range = None):
        if range == None:
            range = 0.1 * value
        
        min = value - range
        max = value + range
        return RandomFloat.next_float(min, max)
