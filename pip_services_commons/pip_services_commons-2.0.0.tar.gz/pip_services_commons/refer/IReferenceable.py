# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.IReferenceable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for referenceable components.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IReferenceable:
    """
    Interface for components that requires references to other components
    """

    def set_references(self, references):
        """
        Sets references to other components.
        Using locators the component can find required dependencies 

        Args:
            references: component references
        """
        raise NotImplementedError('Method from interface definition')
