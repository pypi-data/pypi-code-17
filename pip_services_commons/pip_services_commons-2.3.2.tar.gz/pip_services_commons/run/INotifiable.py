# -*- coding: utf-8 -*-
"""
    pip_services_commons.run.INotifiable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for notifiable components with parameters
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class INotifiable:
    """
    Interface for components that support parameterized one-way notification 
    """

    def notify(self, correlation_id, args):
        """
        Executes a unit of work with given parameters

        Args:
            correlation_id: a unique transaction id to trace calls across components
            args: a set of parameters for execution
        
        Raises: ApplicationException on any error
        """
        raise NotImplementedError('Method from interface definition')
