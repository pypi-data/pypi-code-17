# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.ReferenceQuery
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Query object to retrieve specific references
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ReferenceQuery:

    def __init__(self, locator, start_locator = None, ascending = True):
        self.locator = locator
        self.start_locator = start_locator
        self.ascending = ascending
    
    locator = None
    start_locator = None
    ascending = None