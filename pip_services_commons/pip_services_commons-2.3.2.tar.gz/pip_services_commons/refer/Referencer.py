# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.Referencer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Referencer component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IReferenceable import IReferenceable
from .IUnreferenceable import IUnreferenceable

class Referencer:
    """
    Helper class that assigns references to components
    """

    @staticmethod
    def set_references_for_one(references, component):
        """
        Assigns references to components that implement IReferenceable interface  

        Args:
            references: references to be assigned
            component: a component to assign references
        """
        if isinstance(component, IReferenceable):
            component.set_references(references)

    @staticmethod
    def set_references(references, components):
        """
        Assigns references to components that implement IReferenceable interface  

        Args:
            references: references to be assigned
            components: a list of components to assign references
        """
        if components == None:
            return

        for component in components:
            Referencer.set_references_for_one(references, component)

    @staticmethod
    def unset_references_for_one(component):
        """
        Clears references for components that implement IUnreferenceable interface

        Args:
            component: a component to clear references
        """
        if isinstance(component, IUnreferenceable):
            component.unset_references(references)

    @staticmethod
    def unset_references(components):
        """
        Clears references for components that implement IUnreferenceable interface

        Args:
            components: a list of components to clear references
        """
        if components == None:
            return

        for component in components:
            Referencer.unset_references_for_one(component)
