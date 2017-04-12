# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.IClosable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for closable components
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IClosable:
    """
    Interface for components that require explicit closure 
    """

    def close(self, correlation_id):
        """
        Closes component, disconnects it from services, disposes resources

        Args:
            correlation_id: a unique transaction id to trace calls across components

        Raises: ApplicationException on any error
        """
        raise NotImplementedError('Method from interface definition')
