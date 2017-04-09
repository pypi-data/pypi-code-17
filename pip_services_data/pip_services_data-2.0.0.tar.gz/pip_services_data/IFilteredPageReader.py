# -*- coding: utf-8 -*-
"""
    pip_services_data.IFilteredPageReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for filtered paging data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IFilteredPageReader:

    def get_page_by_filter(self, correlation_id, filter, paging, sort = None):
        raise NotImplementedError('Method from interface definition')
