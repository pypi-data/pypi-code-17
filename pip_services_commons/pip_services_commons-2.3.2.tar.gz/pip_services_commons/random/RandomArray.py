# -*- coding: utf-8 -*-
"""
    pip_services_commons.random.RandomArray
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomArray implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

class RandomArray(object):

    @staticmethod
    def pick(values):
        if values == None or len(values) == 0:
            return None

        return random.choice(values)
