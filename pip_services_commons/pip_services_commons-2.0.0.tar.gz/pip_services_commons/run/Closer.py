# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.Closer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Closer component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IClosable import IClosable

class Closer:
    """
    Helper class that closes components
    """

    @staticmethod
    def close_one(correlation_id, component):
        """
        Closes component that implement ICloseable interface

        Args:
            correlation_id: a unique transaction id to trace calls across components
            component: a component to be closed
        """
        if isinstance(component, IClosable):
            component.close(correlation_id)

    @staticmethod
    def close(correlation_id, components):
        """
        Closes components that implement ICloseable interface

        Args:
            correlation_id: a unique transaction id to trace calls across components
            components: a list of components to be closed
        """
        if components == None:
            return

        for component in components:
            Closer.close_one(correlation_id, component)
