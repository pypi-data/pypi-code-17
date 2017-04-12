# -*- coding: utf-8 -*-
"""
    pip_services_container.refer.ManagedReferences
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Managed references implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.refer import References
from pip_services_commons.refer import Referencer
from pip_services_commons.run import IOpenable
from pip_services_commons.run import Opener
from pip_services_commons.run import Closer

from .ReferencesDecorator import ReferencesDecorator
from .BuildReferencesDecorator import BuildReferencesDecorator
from .LinkReferencesDecorator import LinkReferencesDecorator
from .RunReferencesDecorator import RunReferencesDecorator

class ManagedReferences(ReferencesDecorator, IOpenable):
    _references = None
    _builder = BuildReferencesDecorator
    _linker = LinkReferencesDecorator
    _runner = RunReferencesDecorator

    def __init__(self, tuples = None):
        super(ManagedReferences, self).__init__(None, None)

        self._references = References(tuples)
        self._builder = BuildReferencesDecorator(self._references, self)
        self._linker = LinkReferencesDecorator(self._builder, self)
        self._runner = RunReferencesDecorator(self._linker, self)

        self.base_references = self._runner

    def is_opened(self):
        components = self.get_all()
        return Opener.is_opened(components)

    def open(self, correlation_id):
        components = self.get_all()
        Referencer.set_references(self, components)
        Opener.open(correlation_id, components)

    def close(self, correlation_id):
        components = self.get_all()
        Closer.close(correlation_id, components)
        Referencer.unset_references(components)

    @staticmethod
    def from_tuples(*tuples):
        return ManagedReferences(tuples)