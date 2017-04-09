# -*- coding: utf-8 -*-
"""
    pip_services_data.IQuerableReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for querable data readers.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IQuerableReader:

    def get_list_by_query(self, correlation_id, query, sort = None):
        raise NotImplementedError('Method from interface definition')
