# -*- coding: utf-8 -*-
"""
    pip_services_net.messaging.IMessageQeueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for message queues.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.run import IOpenable, IClosable

class IMessageQueue(IOpenable, IClosable):
    
    def get_name(self):
        raise NotImplementedError('Method from interface definition')

    def get_capabilities(self):
        raise NotImplementedError('Method from interface definition')

    def read_message_count(self):
        raise NotImplementedError('Method from interface definition')

    def send(self, correlation_id, envelop):
        raise NotImplementedError('Method from interface definition')

    def send_as_object(self, correlation_id, message_type, message):
        raise NotImplementedError('Method from interface definition')

    def peek(self, correlation_id):
        raise NotImplementedError('Method from interface definition')

    def peek_batch(self, correlation_id, message_count):
        raise NotImplementedError('Method from interface definition')

    def receive(self, correlation_id, wait_timeout):
        raise NotImplementedError('Method from interface definition')

    def renew_lock(self, message, lock_timeout):
        raise NotImplementedError('Method from interface definition')

    def complete(self, message):
        raise NotImplementedError('Method from interface definition')

    def abandon(self, message):
        raise NotImplementedError('Method from interface definition')

    def move_to_dead_letter(self, message):
        raise NotImplementedError('Method from interface definition')

    def listen(self, correlation_id, receiver):
        raise NotImplementedError('Method from interface definition')

    def begin_listen(self, correlation_id, receiver):
        raise NotImplementedError('Method from interface definition')

    def end_listen(self, correlation_id):
        raise NotImplementedError('Method from interface definition')
