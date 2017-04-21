# -*- coding: utf-8 -*-
"""
    pip_services_container.refer.LinkReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Link references decorator implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.refer import IReferences
from pip_services_commons.refer import Referencer
from pip_services_commons.run import IOpenable

from .ReferencesDecorator import ReferencesDecorator

class LinkReferencesDecorator(ReferencesDecorator, IOpenable):
    _opened = False

    def __init__(self, base_references, parent_references):
        super(LinkReferencesDecorator, self).__init__(base_references, parent_references)


    def is_opened(self):
        return self._opened

    def open(self, correlation_id):
        if not self._opened:
            components = self.get_all()
            Referencer.set_references(self.parent_references, components)
            self._opened = True

    def close(self, correlation_id):
        if self._opened:
            components = self.get_all()
            Referencer.unset_references(components)
            self._opened = False


    def put(self, locator, component):
        super(LinkReferencesDecorator, self).put(locator, component)

        if self._opened:
            Referencer.set_references_for_one(self.parent_references, component)


    def remove(self, locator):
        component = super(LinkReferencesDecorator, self).remove(locator)

        if self._opened:
            Referencer.unset_references_for_one(component)

        return component


    def remove_all(self, locator):
        components = super(LinkReferencesDecorator, self).remove_all(locator)

        if self._opened:
            Referencer.unset_references(components)

        return components
