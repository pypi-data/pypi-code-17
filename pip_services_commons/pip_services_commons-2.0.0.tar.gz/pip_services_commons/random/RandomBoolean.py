# -*- coding: utf-8 -*-
"""
    pip_services_commons.random.RandomBoolean
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    RandomBoolean implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random

class RandomBoolean(object):
    
    @staticmethod
    def chance(chances, max_chances):
        chances = chances if chances >= 0 else 0
        max_chances = max_chances if max_chances >= 0 else 0
        if chances == 0 and max_chances == 0:
            return False
        
        max_chances = max(max_chances, chances)
        start = (max_chances - chances) / 2
        end = start + chances
        hit = random.random() * max_chances
        return hit >= start and hit <= end

    @staticmethod
    def next_boolean():
        return random.randint(0, 100) < 50
