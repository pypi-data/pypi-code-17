# -*- coding: utf-8 -*-
"""
    pip_services_logging.logic.LoggingController
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging controller implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.commands import ICommandable
from pip_services_commons.config import ConfigParams, IConfigurable
from pip_services_commons.refer import IReferences, IReferenceable
from pip_services_commons.refer import Descriptor, DependencyResolver
from pip_services_commons.data import FilterParams, PagingParams

from .ILoggingBusinessLogic import ILoggingBusinessLogic
from .LoggingCommandSet import LoggingCommandSet

class LoggingController(object, ILoggingBusinessLogic, ICommandable, IConfigurable, IReferenceable):
    _dependency_resolver = None
    _read_persistence = None
    _write_persistence = []
    _command_set = None

    def __init__(self):
        self._dependency_resolver = DependencyResolver()
        self._dependency_resolver.put('read_persistence', Descriptor('pip-services-logging', 'persistence', '*', '*', '*'))
        self._dependency_resolver.put('write_persistence', Descriptor('pip-services-logging', 'persistence', '*', '*', '*'))
        self._command_set = LoggingCommandSet(self)


    def get_command_set(self):
        return self._command_set

    def configure(self, config):
        self._dependency_resolver.configure(config)

    def set_references(self, references):
        self._dependency_resolver.set_references(references)
        self._read_persistence = self._dependency_resolver.get_one_required('read_persistence')
        self._write_persistence = self._dependency_resolver.get_optional('write_persistence')

    def read_messages(self, correlation_id, filter, paging):
        if self._read_persistence == None: return DatePage([], 0)
        return self._read_persistence.get_page_by_filter(correlation_id, filter, paging)

    def read_errors(self, correlation_id, filter, paging):
        if self._read_persistence == None: return DatePage([], 0)
        filter = filter if filter != None else FilterParams()
        filter.set_as_object('errors_only', True)
        return self._read_persistence.get_page_by_filter(correlation_id, filter, paging)

    def write_message(self, correlation_id, message):
        if self._write_persistence == None: return message
        for persistence in self._write_persistence:
            persistence.create(correlation_id, message)
        return message

    def write_messages(self, correlation_id, messages):
        if self._write_persistence == None: return
        for persistence in self._write_persistence:
            for message in messages:
                persistence.create(correlation_id, message)

    def clear(self, correlation_id):
        if self._write_persistence == None: return
        for persistence in self._write_persistence:
            persistence.clear(correlation_id)

