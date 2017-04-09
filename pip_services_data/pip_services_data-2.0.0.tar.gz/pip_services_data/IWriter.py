# -*- coding: utf-8 -*-
"""
    pip_services_data.IWriter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data writers.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IWriter:

    def create(self, correlation_id, item):
        raise NotImplementedError('Method from interface definition')

    def update(self, correlation_id, item):
        raise NotImplementedError('Method from interface definition')

    def delete_by_id(self, correlation_id, id):
        raise NotImplementedError('Method from interface definition')
