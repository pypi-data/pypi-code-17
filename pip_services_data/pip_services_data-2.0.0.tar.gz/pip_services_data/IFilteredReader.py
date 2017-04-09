# -*- coding: utf-8 -*-
"""
    pip_services_data.IFilteredReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for filtered data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IFilteredReader:

    def get_list_by_filter(self, correlation_id, filter, sort = None):
        raise NotImplementedError('Method from interface definition')
