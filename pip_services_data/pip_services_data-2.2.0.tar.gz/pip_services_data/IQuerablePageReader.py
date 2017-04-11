# -*- coding: utf-8 -*-
"""
    pip_services_data.IQuerablePageReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for querable paging data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IQuerablePageReader:

    def get_page_by_query(self, correlation_id, query, paging, sort = None):
        raise NotImplementedError('Method from interface definition')
