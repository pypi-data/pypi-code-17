# -*- coding: utf-8 -*-
"""
    pip_services_data.ILoader
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data loaders.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ILoader:

    def load(self, correlation_id):
        raise NotImplementedError('Method from interface definition')
