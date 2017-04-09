# -*- coding: utf-8 -*-
"""
    pip_services_data.IPartialUpdater
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for partial data updaters.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IPartialUpdater:

    def update_partially(self, correlation_id, id, data):
        raise NotImplementedError('Method from interface definition')
