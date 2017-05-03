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

"""Selenol backend connections."""

import json
import time

import websocket

from .exceptions import SelenolWebSocketClosedException


class SelenolWSConnection(object):
    """Selenol websocket client connection with backend."""

    def __init__(self, server=None):
        """Selenol WebSocket connection constructor.

        :param server: String WS server connection.
        """
        server = server or "ws://localhost:9765"
        self.ws = websocket.create_connection(server)

    def send(self, message):
        """Send a the defined message to the backend.

        :param message: Message to be send, usually a Python dictionary.
        """
        try:
            self.ws.send(json.dumps(message))
        except websocket._exceptions.WebSocketConnectionClosedException:
            raise SelenolWebSocketClosedException()

    def recv(self):
        """Receive message from the backend or wait unilt next message."""
        try:
            message = self.ws.recv()
            return json.loads(message)
        except websocket._exceptions.WebSocketConnectionClosedException as ex:
            raise SelenolWebSocketClosedException() from ex

    def close(self):
        """Close the WebSocket connection."""
        self.ws.close()
