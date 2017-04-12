# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.ICommand
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for commands.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..run.IParamExecutable import IParamExecutable

class ICommand(object, IParamExecutable):
    """
    Interface for commands that execute functional operations.
    """

    def get_name(self):
        """
        Gets the command name.

        Results: the command name
        """
        raise NotImplementedError('Method from interface definition')

    def validate(self, args):
        """
        Performs validation of the command arguments.
        
        Args:
            args: command arguments

        Returns: a list of validation results
        """
        raise NotImplementedError('Method from interface definition')
    