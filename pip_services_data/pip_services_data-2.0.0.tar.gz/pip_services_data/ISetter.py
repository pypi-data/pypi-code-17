# -*- coding: utf-8 -*-
"""
    pip_services_data.ISetter
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data setters.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ISetter:

    def set(self, correlation_id, item):
        raise NotImplementedError('Method from interface definition')
