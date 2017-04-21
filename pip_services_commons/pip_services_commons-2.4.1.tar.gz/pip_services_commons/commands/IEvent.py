# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.IEvent
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for events.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..run.IParamNotifiable import IParamNotifiable

class IEvent(object, IParamNotifiable):
    """
    Interface for command events.
    """

    def get_name(self):
        """
        Gets the event name.
        Returns: the event name
        """
        raise NotImplementedError('Method from interface definition')

    def get_listeners(self):
        """
        Get listeners that receive notifications for that event
        Returns: a list with listeners
        """
        raise NotImplementedError('Method from interface definition')

    def add_listener(self, listener):
        """
        Adds listener to receive notifications

        Args:
            listener: a listener reference to be added
        """
        raise NotImplementedError('Method from interface definition')

    def remove_listener(self, listener):
        """
        Removes listener for event notifications.

        Args:
            listener: a listener reference to be removed
        """
        raise NotImplementedError('Method from interface definition')
    