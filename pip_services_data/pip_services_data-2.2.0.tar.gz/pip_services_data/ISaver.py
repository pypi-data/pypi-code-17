# -*- coding: utf-8 -*-
"""
    pip_services_data.ISaver
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for data saver.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ISaver:

    def save(self, correlation_id, items):
        raise NotImplementedError('Method from interface definition')
