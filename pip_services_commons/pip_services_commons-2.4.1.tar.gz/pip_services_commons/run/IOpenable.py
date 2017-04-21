# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.IOpenable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for openable components
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IClosable import IClosable

class IOpenable(IClosable):
    """
    Interface for components that require explicit opening
    """

    def is_opened(self):
        """
        Checks if component is opened

        Returns: True is component is opened and False otherwise
        """
        raise NotImplementedError('Method from interface definition')

    def open(self, correlation_id):
        """
        Opens component, establishes connections to services

        Args:
            correlation_id: a unique transaction id to trace calls across components
        
        Raises: ApplicationException on any error
        """
        raise NotImplementedError('Method from interface definition')
