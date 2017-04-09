# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.Cleaner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cleaner component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICleanable import ICleanable

class Cleaner:
    """
    Helper class that cleans components
    """

    @staticmethod
    def clear_one(correlation_id, component):
        """
        Cleans component that implements ICleanable interface

        Args:
            correlation_id: a unique transaction id to trace calls across components
            component: a component to be cleaned
        """
        if isinstance(component, ICleanable):
            component.clear(correlation_id)

    @staticmethod
    def clear(correlation_id, components):
        """
        Cleans components that implement ICleanable interface

        Args:
            correlation_id: a unique transaction id to trace calls across components
            components: a list of components to be cleaned
        """
        if components == None:
            return

        for component in components:
            Cleaner.clear_one(correlation_id, component)
