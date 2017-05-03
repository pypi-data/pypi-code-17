# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Abstract Selenol service declaration."""

import logging

from .connections import SelenolWSConnection
from .data_structures import SelenolMessage
from .exceptions import *
from .persistences import session_creator


class SelenolClient(object):
    """Selenol basic client connection."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        self.connection = connection or SelenolWSConnection()
        self.session = session or session_creator()
        self.on_open()

    def run(self):
        """Run the service in infinitive loop processing requests."""
        try:
            while True:
                message = self.connection.recv()
                result = self.on_message(message)
                if result:
                    self.connection.send(result)
        except SelenolWebSocketClosedException as ex:
            self.on_closed(0, '')
            raise SelenolWebSocketClosedException() from ex

    def on_open(self):
        """Backend connection has been successfully opened."""

    def on_closed(self, code, reason):
        """Backend connectionhas been closed.

        :param code: Numeric code for closing the connection.
        :param reason: String with the connection close reason.
        """

    def on_message(self, message):
        """Message from the backend has been received.

        :param message: Message string received.
        """
        raise NotImplementedError()

    def send(self, reason, message):
        """Send a message to the backend.

        :param reason: Reason of the message.
        :param message: Message content.
        """
        self.connection.send({
            'reason': reason,
            'content': message,
        })

    def notify(self, topic, message):
        """Send a message to all the subcribers of the topic.

        :param topic: Target topic for the message.
        :param message: Message to be sent.
        """
        self.connection.send({
            'reason': ['request', 'notification'],
            'content': {
                'topic': topic,
                'content': message,
            },
        })


class SelenolService(SelenolClient):
    """Abstract Selenol service implementation."""

    def __init__(self, reason, connection=None, session=None):
        """Constructor.

        :param reason: Type of requests that the service processes.
        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(SelenolService, self).__init__(connection, session)
        self.request_counter = 0
        register = {
            'reason': ["request", "register"],
            'request_id': 0,
            'content': {
                'reason': reason,
            },
        }
        self.connection.send(register)

    def on_message(self, message):
        """Message from the backend has been received.

        :param message: Message string received.
        """
        work_unit = SelenolMessage(message)
        request_id = work_unit.request_id

        if message['reason'] == ['selenol', 'request']:
            try:
                result = self.on_request(work_unit)
                if result is not None:
                    return {
                        'reason': ['request', 'result'],
                        'request_id': request_id,
                        'content': {
                            'content': result,
                        },
                    }
            except SelenolException as e:
                logging.exception(e)
                return {
                    'reason': ['request', 'exception'],
                    'request_id': request_id,
                    'content': {
                        'message': str(e),
                    },
                }
            except Exception as e:
                logging.exception(e)
                return {
                    'reason': ['request', 'exception'],
                    'request_id': request_id,
                    'content': {
                        'message': 'Not a Selenol exception',
                    },
                }

    def on_request(self, message):
        """Request to be processed.

        :param message: Message containing the request.
        """
        raise NotImplementedError()

    def metadata(self, request_id, content):
        """Store metadata for the session that has executed the request.

        :param request_id: Request ID of a involved session.
        :param content: Content to be stored.
        """
        self.connection.send({
            'reason': ['request', 'metadata'],
            'request_id': request_id,
            'content':  content,
        })

    def event(self, request_id, trigger, event, message):
        """Create an event in the backend to be triggered given a circumstance.

        :param request_id: Request ID of a involved session.
        :param trigger: Circumstance that will trigger the event.
        :param event: Reason of the message that will be created.
        :param message: Content of the message that will be created.
        """
        self.connection.send({
            'reason': ['request', 'event'],
            'request_id': request_id,
            'content': {
                'trigger': trigger,
                'message': {
                    'reason': event,
                    'content': message,
                },
            },
        })

    def send(self, event, message):
        """Send a message to the backend.

        :param reason: Reason of the message.
        :param message: Message content.
        """
        self.connection.send({
            'reason': ['request', 'send'],
            'content': {
                'reason': event,
                'request_id': self.request_counter,
                'content': message,
            },
        })
        self.request_counter = self.request_counter + 1
