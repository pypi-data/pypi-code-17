# -*- coding: utf-8 -*-
"""
    tests.messaging.test_MemoryMessageQueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import pytest

from pip_services_net.messaging import MemoryMessageQueue
from .MessageQueueFixture import MessageQueueFixture

class TestMemoryMessageQueue:
    queue = None
    fixture = None

    @classmethod
    def setup_class(cls):
        cls.queue = MemoryMessageQueue()
        cls.fixture = MessageQueueFixture(cls.queue)

    def setup_method(self, method):
        self.queue.clear(None)
        self.queue.open(None)

    def teardown_method(self, method):
        self.queue.close(None)

    def test_send_receive_message(self):
        self.fixture.test_send_receive_message()

    def test_receive_send_message(self):
        self.fixture.test_receive_send_message()

    def test_move_to_dead_message(self):
        self.fixture.test_move_to_dead_message()

    def test_receive_and_complete_message(self):
        self.fixture.test_receive_and_complete_message()

    def test_receive_and_abandon_message(self):
        self.fixture.test_receive_and_abandon_message()

    def test_send_peek_message(self):
        self.fixture.test_send_peek_message()

    def test_peek_no_message(self):
        self.fixture.test_peek_no_message()

    def test_listen(self):
        self.fixture.test_listen()
