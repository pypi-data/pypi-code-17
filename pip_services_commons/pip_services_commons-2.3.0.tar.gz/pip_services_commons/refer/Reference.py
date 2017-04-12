# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.Reference
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Reference component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class Reference(object):
    """
    Placeholder to store component references.
    """

    _locator = None
    _component = None


    def __init__(self, locator, component):
        if component == None:
            raise Exception("Component cannot be null")
        
        self._locator = locator
        self._component = component


    def match(self, locator):
        # Locate by direct reference matching
        if self._component == locator:
            return True
        # Locate by direct locator matching
        elif self._locator != None:
            return self._locator == locator
        else:
            return False


    def get_component(self):
        return self._component


    def get_locator(self):
        return self._locator
