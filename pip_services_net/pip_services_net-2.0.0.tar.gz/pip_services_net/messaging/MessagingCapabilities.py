# -*- coding: utf-8 -*-
"""
    pip_services_net.messaging.MessagingCapabilities
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Messaging capabilities implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class MessagingCapabilities(object):
    _message_count = None
    _send = None
    _receive = None
    _peek = None
    _peek_batch = None
    _renew_lock = None
    _abandon = None
    _dead_letter = None
    _clear = None

    def __init__(self, message_count, send, receive, peek, peek_batch, renew_lock, abandon, dead_letter, clear):
        self._message_count = message_count
        self._send = send
        self._receive = receive
        self._peek = peek
        self._peek_batch = peek_batch
        self._renew_lock = renew_lock;
        self._abandon = abandon
        self._dead_letter = dead_letter
        self._clear = clear

    def can_message_count(self):
        return self._message_count

    def can_send(self):
        return self._send

    def can_receive(self):
        return self._receive

    def can_peek(self):
        return self._peek

    def can_peek_batch(self):
        return self._peek_batch

    def can_renew_lock(self):
        return self._renew_lock

    def can_abandon(self):
        return self._abandon

    def can_dead_letter(self):
        return self._dead_letter

    def can_clear(self):
        return self._clear
