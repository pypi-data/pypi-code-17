# -*- coding: utf-8 -*-
"""
    pip_services_container.refer.ReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    References decorator implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.refer import IReferences

class ReferencesDecorator(object, IReferences):
    base_references = None
    parent_references = None

    def __init__(self, base_references, parent_references):
        self.base_references = base_references if base_references != None else parent_references
        self.parent_references = parent_references if parent_references != None else base_references


    def put(self, locator, component):
        self.base_references.put(locator, component)

    def remove(self, locator):
        return self.base_references.remove(locator)

    def remove_all(self, locator):
        return self.base_references.remove_all(locator)

    def get_all(self):
        return self.base_references.get_all()
        
    def get_one_optional(self, locator):
        try:
            components = self.find(locator, False)
            return components[0] if len(components) > 0 else None
        except Exception as ex:
            return None

    def get_one_required(self, locator):
        components = self.find(locator, True)
        return components[0] if len(components) > 0 else None

    def get_optional(self, locator):
        try:
            return self.find(locator, False)
        except Exception as ex:
            return []

    def get_required(self, locator):
        return self.find(locator, True)

    def find(self, locator, required):
        return self.base_references.find(locator, required)
