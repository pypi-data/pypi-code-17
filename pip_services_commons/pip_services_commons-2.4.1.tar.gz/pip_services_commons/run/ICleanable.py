# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.ICleanable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for cleanable components
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICleanable:

    def clear(self, correlation_id):
        raise NotImplementedError('Method from interface definition')
