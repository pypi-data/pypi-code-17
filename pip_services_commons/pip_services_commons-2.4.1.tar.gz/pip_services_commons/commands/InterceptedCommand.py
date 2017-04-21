# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.InterceptedCommand
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Intercepted command implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICommand import ICommand

class InterceptedCommand(ICommand):
    """
    Interceptor wrapper to turn it into stackable command
    """

    _intercepter = None
    _next = None

    def __init__(self, intercepter, next):
        """
        Creates instance of intercepted command by chaining
        intercepter with the next intercepter in the chain 
        or command at the end of the chain.
        
        Args:
            intercepter: the intercepter reference.
            next: the next intercepter or command in the chain.
        """
        self._intercepter = intercepter
        self._next = next

    def get_name(self):
        """
        Gets the command name.
        Results: the command name
        """
        return self._intercepter.get_name(_next)

    def execute(self, correlation_id, args):
        """
        Executes the command given specific arguments as an input.
        
        Args:
            correlation_id: a unique correlation/transaction id
            args: command arguments
        
        Returns: an execution result.
        
        Raises:
            MicroserviceError: when execution fails for whatever reason.
        """
        return self._intercepter.execute(_next, correlation_id, args)

    def validate(self, args):
        """
        Performs validation of the command arguments.
        
        Args:
            args: command arguments
        
        Returns: a list of validation results
        """
        return self._intercepter.validate(self._next, args)
    