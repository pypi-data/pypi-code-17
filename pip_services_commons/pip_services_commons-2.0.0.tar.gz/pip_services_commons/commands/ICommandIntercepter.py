# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.ICommandIntercepter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for command intercepters.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICommandIntercepter(object):
    """
    Interface for stackable command intercepters.
    """

    def get_name(self, command):
        """
        Gets the command name. Intercepter can modify the name if needed

        Args:
            command: intercepted ICommand

        Results: the command name
        """
        raise NotImplementedError('Method from interface definition')

    def execute(self, correlation_id, command, args):
        """
        Executes the command given specific arguments as an input.
        
        Args:
            correlation_id: a unique correlation/transaction id
            command: intercepted ICommand
            args: command arguments
        
        Returns: an execution result.
        
        Raises:
            ApplicationException when execution fails for whatever reason.
        """
        raise NotImplementedError('Method from interface definition')

    def validate(command, args):
        """
        Performs validation of the command arguments.
        
        Args:
            command: intercepted ICommand
            args: command arguments
        
        Returns: a list of validation results.
        """
        raise NotImplementedError('Method from interface definition')
    