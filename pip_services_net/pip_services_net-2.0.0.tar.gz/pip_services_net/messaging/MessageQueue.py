# -*- coding: utf-8 -*-
"""
    pip_services_net.messaging.MessageQeueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract message queue implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading

from pip_services_commons.config import IConfigurable, NameResolver
from pip_services_commons.refer import IReferenceable
from pip_services_commons.run import IOpenable
from pip_services_commons.log import CompositeLogger
from pip_services_commons.count import CompositeCounters
from pip_services_commons.auth import CredentialResolver
from pip_services_commons.connect import ConnectionResolver

from .MessageEnvelop import MessageEnvelop

class MessageQueue(object, IConfigurable, IReferenceable, IOpenable):
    _name = None
    _capabilities = None
    _lock = None
    _logger = None
    _counters = None
    _credential_resolver = None
    _connection_resolver = None

    def __init__(self, name = None):
        self._lock = threading.Lock()
        self._logger = CompositeLogger()
        self._counters = CompositeCounters()
        self._connection_resolver = ConnectionResolver()
        self._credential_resolver = CredentialResolver()
        self._name = name


    def configure(self, config):
        self._name = NameResolver.resolve(config)
        self._logger.configure(config)
        self._credential_resolver.configure(config)
        self._connection_resolver.configure(config)


    def set_references(self, references):
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._credential_resolver.set_references(references)
        self._connection_resolver.set_references(references)


    def open(self, correlation_id):
        connection = self._connection_resolver.resolve(correlation_id)
        credential = self._credential_resolver.lookup(correlation_id)
        self._open_with_params(correlation_id, connection, credential)


    def _open_with_params(self, correlation_id, connection, credential):
        raise NotImplementedError('Abstract method that shall be overriden')


    def get_name(self):
        return self._name if self._name != None else "undefined"


    def get_capabilities(self):
        return self._capabilities


    def send_as_object(self, correlation_id, message_type, message):
        envelop = MessageEnvelop(correlation_id, message_type, message)
        self.send(correlation_id, envelop)


    def begin_listen(self, correlation_id, receiver):
        # Start listening on a parallel tread
        thread = threading.Thread(target=self.listen, args=(correlation_id, receiver))
        thread.daemon = True
        thread.start()


    def __str__(self):
        return "[" + self.get_name() + "]"
