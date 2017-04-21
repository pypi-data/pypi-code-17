# -*- coding: utf-8 -*-
"""
    pip_services_container.Component
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.config import IConfigurable
from pip_services_commons.log import CompositeLogger
from pip_services_commons.count import CompositeCounters
from pip_services_commons.refer import IReferenceable
from pip_services_commons.refer import DependencyResolver

class Component(object, IConfigurable, IReferenceable):
    _logger = None
    _counters = None
    _dependency_resolver = None

    def __init__(self):
        self._logger = CompositeLogger()
        self._counters = CompositeCounters()
        self._dependency_resolver = DependencyResolver()

    def configure(self, config):
        self._dependency_resolver.configure(config)
        self._logger.configure(config)

    def set_references(self, references):
        self._dependency_resolver.set_references(references)
        self._logger.set_references(references)
        self._counters.set_references(references)
