# -*- coding: utf-8 -*-
"""
    pip_services_commons.build.IFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for factory components.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IFactory:

    def can_create(self, locator):
        raise NotImplementedError('Method from interface definition')

    def create(self, locator):
        raise NotImplementedError('Method from interface definition')