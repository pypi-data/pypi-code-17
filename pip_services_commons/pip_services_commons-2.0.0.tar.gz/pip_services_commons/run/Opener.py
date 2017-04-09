# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.Opener
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Opener component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IOpenable import IOpenable

class Opener:
    """
    Helper class that opens a collection of components 
    """


    @staticmethod
    def is_opened_one(component):
        """
        Checks if component that implements IOpenable interface is opened

        Args:
            component: a components to be checked
        """
        if isinstance(component, IOpenable):
            return component.is_opened()

        return True

    @staticmethod
    def is_opened(components):
        """
        Checks if all components that implement IOpenable interface are opened

        Args:
            components: a list of components to be checked
        """
        if components == None:
            return True

        result = True
        for component in components:
            result = result and Opener.is_opened_one(component)

        return result

    @staticmethod
    def open_one(correlation_id, component):
        """
        Opens a component that implements IOpenable interface

        Args:
            correlation_id: a unique transaction id to trace calls across components
            component: a components to be opened
        """
        if isinstance(component, IOpenable):
            component.open(correlation_id)

    @staticmethod
    def open(correlation_id, components):
        """
        Opens components that implement IOpenable interface

        Args:
            correlation_id: a unique transaction id to trace calls across components
            components: a list of components to be opened
        """
        if components == None:
            return

        for component in components:
            Opener.open_one(correlation_id, component)
