# -*- coding: utf-8 -*-
"""
    pip_services_commons.commands.CommandSet
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Command set implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..errors.BadRequestException import BadRequestException
from ..validate.ValidationException import ValidationException
from ..validate.ValidationResult import ValidationResult
from ..validate.ValidationResultType import ValidationResultType
from ..data.IdGenerator import IdGenerator

class CommandSet(object):
    """
    Handles command registration and execution.
    Enables intercepters to control or modify command behavior 
    """

    _commands = None
    _commands_by_name = None
    _events = None
    _events_by_name = None
    _intercepters = None

    def __init__(self):
        self._commands = []
        self._commands_by_name = {}
        self._events = []
        self._events_by_name = {}
        self._intercepters = []

    def get_commands(self):
        """
        Get all supported commands
        Returns: ICommand list with all commands supported by component. 
        """
        return self._commands

    def get_events(self):
        """
        Get all supported events
        Returns: ICommand list with all events supported by component. 
        """
        return self._events

    def find_command(self, command):
        """
        Find a specific command by its name.
        
        Args:
            command: the command name.

        Returns: found ICommand or None
        """
        if command in self._commands_by_name:
            return self._commands_by_name[command]
        else:
            return None

    def find_event(self, event):
        """
        Find a specific event by its name.
        
        Args:
            event: the event name.

        Returns: found IEvent or None
        """
        if event in self._events_by_name:
            return self._events_by_name[event]
        else:
            return None

    def _build_command_chain(self, command):
        """
        Builds execution chain including all intercepters and the specified command.

        Args:
            command: the command to build a chain.

        Returns: None
        """
        next = command
        for intercepter in reversed(self._intercepters):
            next = InterceptedCommand(intercepter, next)
        self._commands_by_name[next.get_name()] = next

    def _rebuild_all_command_chains(self):
        """
        Rebuilds execution chain for all registered commands.
        This method is typically called when intercepters are changed.
        Because of that it is more efficient to register intercepters
        before registering commands (typically it will be done in abstract classes).
        However, that performance penalty will be only once during creation time.

        Returns: None 
        """
        self._commands_by_name = {}
        for command in self._commands:
            self._build_command_chain(command)

    def add_command(self, command):
        """
        Adds a command to the command set.
        
        Args:
            command: a command instance to be added

        Returns: None
        """
        self._commands.append(command)
        self._build_command_chain(command)

    def add_commands(self, commands):
        """
        Adds a list of commands to the command set
        
        Args:
            commands: a list of commands to be added

        Returns: None
        """
        for command in commands:
            self.add_command(command)

    def add_event(self, event):
        """
        Adds an eventr to the command set.
        
        Args:
            event: an event instance to be added

        Returns: None
        """
        self._events.append(event)
        self._events_by_name[event.get_name] = event

    def add_events(self, events):
        """
        Adds a list of eventrs to the command set
        
        Args:
            events: a list of events to be added

        Returns: None
        """
        for event in events:
            self.add_event(event)

    def add_command_set(self, command_set):
        """
        Adds commands and events from another command set to this one
        
        Args:
            command_set: a commands set to add commands from

        Returns: None
        """
        for command in command_set.get_commands():
            self.add_command(command)

        for event in command_set.get_events():
            self.add_event(event)

    def add_intercepter(self, intercepter):
        """
        Adds intercepter to the command set.
        
        Args:
            intercepter: an intercepter instance to be added.

        Returns: None
        """
        self._intercepters.append(intercepter)
        self._rebuild_all_command_chains()

    def execute(self, correlation_id, command, args):
        """
        Execute command by its name with specified arguments.
        
        Args:
            correlation_id: a unique correlation/transaction id
            command: the command name.
            args: a list of command arguments.
        
        Returns: the execution result.
        
        Raises:
            MicroserviceError: when execution fails for any reason.
        """
        # Get command and throw error if it doesn't exist
        cref = self.find_command(command)
        if cref == None:
            raise BadRequestException(
                correlation_id,
                "CMD_NOT_FOUND",
                "Requested command does not exist"
            ).with_details("command", command)

        # Generate correlationId if it doesn't exist
        # Use short ids for now
        if correlation_id == None:
           correlation_id = IdGenerator.next_short()
        
        # Validate command arguments before execution and throw the 1st found error
        results = cref.validate(args)
        ValidationException.throw_exception_if_needed(correlation_id, results, False)
                
        # Execute the command.
        return cref.execute(correlation_id, args)

    def validate(self, command, args):
        """
        Validates command arguments.
        
        Args:
            command: the command name.
            args: a list of command arguments.
        
        Returns: list with validation results
        """
        cref = self.find_command(command)
        if cref == None:
            results = []
            results.append( \
                ValidationResult(
                    None, ValidationResultType.Error,
                    "CMD_NOT_FOUND", 
                    "Requested command does not exist"
                )
            )
            return results

        return cref.validate(args)
    
    def add_listener(self, listener):
        """
        Adds listener to all events.

        Args:
            listener: a listener to be added
        """
        for event in self._events:
            event.add_listener(listener)

    def remove_listener(self, listener):
        """
        Remove listener to all events.

        Args:
            listener: a listener to be removed
        """
        for event in self._events:
            event.remove_listener(listener)

    def notify(self, correlation_id, event, value):
        """
        Notifies all listeners about the event.

        Args:
            correlation_id: a unique correlation/transaction id
            event: an event name
            value: an event value
        """
        e = self.find_event(event)
        if e != None:
            e.notify(correlation_id, value)
