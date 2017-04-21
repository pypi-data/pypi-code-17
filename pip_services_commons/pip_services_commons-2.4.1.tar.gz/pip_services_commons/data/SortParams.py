# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.SortParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Sort params implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class SortParams(list):

    def __init__(self, **fields):
        for field in fields:
            self.append(field)
