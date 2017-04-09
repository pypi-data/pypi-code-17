# -*- coding: utf-8 -*-
"""
    pip_services_commons.refer.IUnreferenceable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for unreferenceable components.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IUnreferenceable:
    """
    Interface for components that require clear of references to other components
    """

    def unset_references(self):
        """
        Unsets previously set references to other components. 
        """
        raise NotImplementedError('Method from interface definition')
