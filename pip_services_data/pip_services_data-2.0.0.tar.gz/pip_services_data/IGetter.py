# -*- coding: utf-8 -*-
"""
    pip_services_data.IGetter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data getters.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IGetter:

    def get_one_by_id(self, correlation_id, id):
        raise NotImplementedError('Method from interface definition')
