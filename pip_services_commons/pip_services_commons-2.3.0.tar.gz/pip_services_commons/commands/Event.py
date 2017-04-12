# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.Event
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Event implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IEvent import IEvent
from ..errors.InvocationException import InvocationException

class Event(IEvent):
    """
    Events to receive notifications on command execution results and failures.
    """

    _name = None
    _listeners = None

    def __init__(self, name):
        """
        Creates and initializes instance of the event.

        Args:
            name: name of the event
        """
        if name == None:
            raise Exception("Event name is not set")

        self._name = name
        self_listeners = []

    def get_name(self):
        """
        Gets the event name.
        Returns: the event name
        """
        return self._name

    def get_listeners(self):
        """
        Get listeners that receive notifications for that event
        Returns: a list with listeners
        """
        return list(self._listeners)

    def add_listener(self, listener):
        """
        Adds listener to receive notifications

        Args:
            listener: a listener reference to be added
        """
        self._listeners.append(listener)

    def remove_listener(self, listener):
        """
        Removes listener for event notifications.

        Args:
            listener: a listener reference to be removed
        """
        self._listeners.append(remove)
    
    def notify(self, correlation_id, args):
        """
        Notifies all listeners about the event.

        Args:
            correlation_id: a unique correlation/transaction id
            args: an event parameters
        """
        for listener in self._listeners:
            try:
                listener.on_event(correlation_id, self, args)
            except Exception as ex:
                raise InvocationException(
                    correlation_id,
                    "EXEC_FAILED",
                    "Raising event " + self._name + " failed: " + str(ex)
                ).with_details("event", self._name).wrap(ex)
