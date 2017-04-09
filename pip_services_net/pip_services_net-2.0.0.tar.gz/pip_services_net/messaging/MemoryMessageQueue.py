# -*- coding: utf-8 -*-
"""
    pip_services_net.messaging.MemoryMessageQueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory message queue implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading

from pip_services_commons.run import ICleanable
from .MessageEnvelop import MessageEnvelop
from .MessagingCapabilities import MessagingCapabilities
from .MessageQueue import MessageQueue

class MemoryMessageQueue(MessageQueue, ICleanable):
    _default_lock_timeout = 30000
    _default_wait_timeout = 5000

    _event = None
    _messages = None
    _lock_token_sequence = 0
    _locked_messages = None
    _listening = None
    _opened = False

    class LockedMessage(object):
        #message = None
        lock_expiration = None


    def __init__(self, name = None):
        super(MemoryMessageQueue, self).__init__(name)
        self._event = threading.Event()
        self._capabilities = MessagingCapabilities(True, True, True, True, True, True, True, False, True)

        self._messages = []
        self._locked_messages = {}


    def is_opened(self):
        return self._opened

    def _open_with_params(self, correlation_id, connection, credentials):
        self._opened = True
        self._logger.trace(correlation_id, "Opened queue " + str(self))


    def close(self, correlation_id):
        self._opened = False
        self._listening = False 
        self._event.set()
        self._logger.trace(correlation_id, "Closed queue " + str(self))


    def read_message_count(self):
        self._lock.acquire()
        try:
            return len(self._messages)
        finally:
            self._lock.release()


    def send(self, correlation_id, message):
        if message == None: return

        self._lock.acquire()
        try:
            # Add message to the queue
            self._messages.append(message)
        finally:
            self._lock.release()

        # Release threads waiting for messages
        self._event.set()
        
        self._counters.increment_one("queue." + self.get_name() + ".sent_messages")
        self._logger.debug(correlation_id, "Sent message " + str(message) + " via " + str(self))


    def peek(self, correlation_id):
        message = None

        self._lock.acquire()
        try:
            # Pick a message
            if len(self._messages) > 0:
                message = self._messages[0]
        finally:
            self._lock.release()

        if message != None:
            self._logger.trace(correlation_id, "Peeked message " + str(message) + " on " + str(self))

        return message


    def peek_batch(self, correlation_id, message_count):
        messages = []

        self._lock.acquire()
        try:
            index = 0
            while index < len(self._messages) and index < message_count:
                messages.append(self._messages[index])
                index += 1
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Peeked " + str(len(messages)) + " messages on " + str(self))

        return messages


    def receive(self, correlation_id, wait_timeout):
        message = None

        self._lock.acquire()
        try:
            # Try to get a message
            if len(self._messages) > 0:
                message = self._messages[0]
                del self._messages[0]
            else:
                self._event.clear()
        finally:
            self._lock.release()

        if message == None:
            self._event.wait(wait_timeout)

        self._lock.acquire()
        try:
            # Try to get a message again
            if message == None and len(self._messages) > 0:
                message = self._messages[0]
                del self._messages[0]
            
            # Exit if message was not found
            if message == None:
                return None

            # Generate and set locked token
            locked_token = self._lock_token_sequence
            self._lock_token_sequence += 1
            message.reference = locked_token

            # Add messages to locked messages list
            locked_message = self.LockedMessage()
            locked_message.lock_expiration = time.clock() + (float(self._default_lock_timeout) / 1000.)
            #locked_message.message = message

            self._locked_messages[locked_token] = locked_message
        finally:
            self._lock.release()

        self._counters.increment_one("queue." + self.get_name() + ".received_messages")
        self._logger.debug(message.correlation_id, "Received message " + str(message) + " on " + str(self))

        return message


    def renew_lock(self, message, lock_timeout):
        if message == None or message.reference == None: 
            return

        self._lock.acquire()
        try:
            # Get message from locked queue
            locked_token = message.reference
            locked_message = self._locked_messages[locked_token]

            # If lock is found, extend the lock
            if locked_message != None:
                locked_message.lock_expiration = time.clock() + (float(lock_timeout) / 1000.)
        finally:
            self._lock.release()

        self._logger.trace(message.correlation_id, "Renewed lock for message " + str(message) + " at " + str(self))


    def abandon(self, message):
        if message == None or message.reference == None: 
            return

        self._lock.acquire()
        try:
            # Get message from locked queue
            locked_token = message.reference
            locked_message = self._locked_messages[locked_token]
            if locked_message != None:
                # Remove from locked messages
                del self._locked_messages[locked_token]
                message.reference = None

                # Skip if it is already expired
                if locked_message.lock_expiration <= time.clock():
                    return
            # Skip if it absent
            else:
                return
        finally:
            self._lock.release()

        self._logger.trace(message.correlation_id, "Abandoned message " + str(message) + " at " + str(self))

        # Add back to the queue
        self.send(message.correlation_id, message)


    def complete(self, message):
        if message == None or message.reference == None: 
            return

        self._lock.acquire()
        try:
            lock_key = message.reference
            del self._locked_messages[lock_key]
            message.reference = None
        finally:
            self._lock.release()

        self._logger.trace(message.correlation_id, "Completed message " + str(message) + " at " + str(self))


    def move_to_dead_letter(self, message):
        if message == None or message.reference == None:
            return

        self._lock.acquire()
        try:
            lock_key = message.reference
            del self._locked_messages[lock_key]
            message.reference = None
        finally:
            self._lock.release()

        self._counters.increment_one("queue." + self.get_name() + ".dead_messages")
        self._logger.trace(message.correlation_id, "Moved to dead message " + str(message) + " at " + str(self))


    def listen(self, correlation_id, receiver):
        if self._listening:
            self._logger.error(correlation_id, "Already listening queue " + str(self))
            return
        
        self._logger.trace(correlation_id, "Started listening messages at " + str(self))

        self._listening = True

        while self._listening:
            message = self.receive(correlation_id, self._default_wait_timeout)

            if self._listening and message != None:
                try:
                    receiver.receive_message(message, self)
                except Exception as ex:
                    self._logger.error(correlation_id, ex, "Failed to process the message")
                    #self.abandon(message)
        
        self._logger.trace(correlation_id, "Stopped listening messages at " + str(self))


    def end_listen(self, correlation_id):
        self._listening = False


    def clear(self, correlation_id):
        self._lock.acquire()
        try:
            # Clear messages
            self._messages = []
            self._locked_messages = {}
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Cleared queue " + str(self))

