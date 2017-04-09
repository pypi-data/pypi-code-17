# -*- coding: utf-8 -*-
"""
    tests.messaging.MessageQueueFixture
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading
import pytest

from pip_services_net.messaging import IMessageQueue, IMessageReceiver
from pip_services_net.messaging import MessageEnvelop, MessagingCapabilities

class MessageQueueFixture:
    _queue = None

    def __init__(self, queue):
        self._queue = queue

    def test_send_receive_message(self):
        envelop1 = MessageEnvelop("123", "Test", "Test message")
        self._queue.send(None, envelop1)

        count = self._queue.read_message_count()
        assert count > 0

        envelop2 = self._queue.receive(None, 10000)
        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

    def test_receive_send_message(self):
        envelop1 = MessageEnvelop("123", "Test", "Test message")

        def run():
            time.sleep(0.2)
            self._queue.send(None, envelop1)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

        envelop2 = self._queue.receive(None, 10000)
        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

    def test_move_to_dead_message(self):
        envelop1 = MessageEnvelop("123", "Test", "Test message")
        self._queue.send(None, envelop1)

        envelop2 = self._queue.receive(None, 10000)
        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

        self._queue.move_to_dead_letter(envelop2)

    def test_receive_and_complete_message(self):
        envelop1 = MessageEnvelop("123", "Test", "Test message")
        self._queue.send(None, envelop1)
        
        envelop2 = self._queue.receive(None, 10000)
        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

        self._queue.complete(envelop2)
        #envelop2 = self._queue.peek(None)
        #assert None == envelop2

    def test_receive_and_abandon_message(self):
        envelop1 = MessageEnvelop("123", "Test", "Test message")
        self._queue.send(None, envelop1)
        
        envelop2 = self._queue.receive(None, 10000)
        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

        self._queue.abandon(envelop2)
        
        envelop2 = self._queue.receive(None, 10000)
        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

    def test_send_peek_message(self):
        envelop1 = MessageEnvelop("123", "Test", "Test message")
        self._queue.send(None, envelop1)
        
        time.sleep(0.2)

        envelop2 = self._queue.peek(None)
        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

    def test_peek_no_message(self):
        envelop = self._queue.peek(None)
        assert None == envelop

    def test_listen(self):
        envelop1 = MessageEnvelop("123", "Test", "Test message")
        envelop2 = MessageEnvelop()

        class TestReceiver (IMessageReceiver):
            def receive_message(self, envelop, queue):
                envelop2.message_id = envelop.message_id
                envelop2.correlation_id = envelop.correlation_id
                envelop2.message_type = envelop.message_type
                envelop2.message = envelop.message

        self._queue.begin_listen(None, TestReceiver())

        self._queue.send(None, envelop1)
        
        time.sleep(0.2)

        assert None != envelop2
        assert envelop1.message_type == envelop2.message_type
        assert envelop1.message == envelop2.message
        assert envelop1.correlation_id == envelop2.correlation_id

        self._queue.end_listen(None)
