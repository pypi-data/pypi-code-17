# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.Command
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Command implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICommand import ICommand
from ..errors.InvocationException import InvocationException

class Command(ICommand):
    """
    Represents a command that implements a command pattern
    """

    _name = None
    _schema = None
    _function = None

    def __init__(self, name, schema, function):
        """
        Creates a command instance
        
        Args:
            component: a component this command belongs to
            name: the name of the command
            schema: a validation schema for command arguments
            function: an execution function to be wrapped into this command.
        """
        if name == None:
            raise TypeError("Command name is not set")
        if function == None:
            raise TypeError("Command function is not set")
        
        self._name = name
        self._schema = schema
        self._function = function

    def get_name(self):
        """
        Gets the command name.
        Results: the command name
        """
        return self._name

    def execute(self, correlation_id, args):
        """
        Executes the command given specific arguments as an input.
        
        Args:
            correlation_id: a unique correlation/transaction id
            args: command arguments
        
        Returns: an execution result.
        
        Raises:
            ApplicationException: when execution fails for whatever reason.
        """
        # Validate arguments
        if self._schema != None:
            self.validate_and_throw_exception(correlation_id, args)
        
        # Call the function
        try:
            return self._function(correlation_id, args)
        # Intercept unhandled errors
        except Exception as ex:
            raise InvocationException(
                correlation_id,
                "EXEC_FAILED",
                "Execution " + self._name + " failed: " + str(ex)
            ).with_details("command", self._name).wrap(ex)


    def validate(self, args):
        """
        Performs validation of the command arguments.
        
        Args:
            args: command arguments
        
        Returns: list with validation results
        """
        # When schema is not defined, then skip validation
        if self._schema != None: 
            return self._schema.validate(args)
        
        # ToDo: Complete implementation
        return []
    