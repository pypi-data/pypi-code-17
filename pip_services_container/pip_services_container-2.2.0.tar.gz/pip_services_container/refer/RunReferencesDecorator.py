# -*- coding: utf-8 -*-
"""
    pip_services_container.refer.RunReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Run references decorator implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.refer import IReferences
from pip_services_commons.run import Opener
from pip_services_commons.run import Closer

from .ReferencesDecorator import ReferencesDecorator

class RunReferencesDecorator(ReferencesDecorator):
    _opened = False

    def __init__(self, base_references, parent_references):
        super(RunReferencesDecorator, self).__init__(base_references, parent_references)


    def is_opened(self):
        return self._opened

    def open(self, correlation_id):
        if not self._opened:
            components = self.get_all()
            Opener.open(correlation_id, components)
            self._opened = True

    def close(self, correlation_id):
        if self._opened:
            components = self.get_all()
            Closer.close(correlation_id, components)
            self._opened = False


    def put(self, locator, component):
        super(RunReferencesDecorator, self).put(locator, component)

        if self._opened:
            Opener.open_one(None, component)


    def remove(self, locator):
        component = super(RunReferencesDecorator, self).remove(locator)

        if self._opened:
            Closer.close_one(None, component)

        return component


    def remove_all(self, locator):
        components = super(RunReferencesDecorator, self).remove_all(locator)

        if self._opened:
            Closer.close(None, components)

        return components
