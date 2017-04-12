# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.IEventListener
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for event listeners.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IEvent import IEvent

class IEventListener(object):
    """
    Listener for command events
    """

    def on_event(self, correlation_id, event, value):
        """
        Notifies that event occurred.

        Args:
            correlation_id: a unique correlation/transaction id
            event: event reference
            value: event arguments
        """
        raise NotImplementedError('Method from interface definition')
