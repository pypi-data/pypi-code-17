# -*- coding: utf-8 -*-
"""
    pip_services_commons.data.SortField
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Sort field implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class SortField:
    name = None
    ascending = True

    def __init__(self, name, ascending = True):
        self.name = name
        self.ascending = ascending
