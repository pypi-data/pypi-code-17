# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.Notifier
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Notifier component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .INotifiable import INotifiable
from .IParamNotifiable import IParamNotifiable
from .Parameters import Parameters

class Notifier:

    @staticmethod
    def notify_one(correlation_id, component, args):
        """
        Triggers notification for components that implement INotifiable interface.

        Args:
            correlation_id: a unique transaction id to trace calls across components
            components:  components a list of components to be notified
            args: a set of parameters to pass to notified components
        """
        if components == None:
            return

        if isinstance(component, INotifiable):
            component.notify(correlation_id, args)

    @staticmethod
    def notify(correlation_id, components, args = None):
        """
        Triggers notification for components that implement INotifiable interface.

        Args:
            correlation_id: a unique transaction id to trace calls across components
            components:  components a list of components to be notified
            args: a set of parameters to pass to notified components
        """
        if components == None:
            return

        args = args if args != None else Parameters()
        for component in components:
            Notifier.notify_one(correlation_id, component, args)
