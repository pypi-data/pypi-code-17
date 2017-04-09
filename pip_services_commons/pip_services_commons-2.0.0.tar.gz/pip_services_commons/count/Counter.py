# -*- coding: utf-8 -*-
"""
    pip_services_commons.counters.Counter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Counter object implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class Counter(object):
    name = None
    type = None
    last = None
    count = None
    min = None
    max = None
    average = None
    time = None

    def __init__(self, name= None, tipe = None):
        self.name = name
        self.type = tipe
