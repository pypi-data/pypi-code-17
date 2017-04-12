# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.ILogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for logging components.
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ILogger:
    """
    Logger that logs messages from other microservice components.
    """

    def get_level(self):
        """
        Get the current level of details

        Returns: the current log level
        """
        raise NotImplementedError('Method from interface definition')

    def set_level(self, level):
        """
        Set the current level of details

        Args:
            level: new logging level

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def log(self, level, correlation_id, error, message, *args, **kwargs):
        """
        Writes message to log

        Args:
            level: a message logging level
            correlation_id: a unique id to identify distributed transaction
            error: error object
            message: a message objects
            args: a list of positional arguments
            kwargs: a list of named arguments

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def fatal(self, correlation_id, error, message, *args, **kwargs):
        """
        Logs fatal error that causes microservice to shutdown
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            error: error object
            message: a message objects
            args: a list of positional arguments
            kwargs: a list of named arguments

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def error(self, correlation_id, error, message, *args, **kwargs):
        """
        Logs recoverable error
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            error: error object
            message: a message objects
            args: a list of positional arguments
            kwargs: a list of named arguments

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def warn(self, correlation_id, message, *args, **kwargs):
        """
        Logs warning messages

        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a message objects
            args: a list of positional arguments
            kwargs: a list of named arguments

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def info(self, correlation_id, message, *args, **kwargs):
        """
        Logs important information message
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a message objects
            args: a list of positional arguments
            kwargs: a list of named arguments

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def debug(self, correlation_id, message, *args, **kwargs):
        """
        Logs high-level debugging messages
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a message objects
            args: a list of positional arguments
            kwargs: a list of named arguments

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def trace(self, correlation_id, message, *args, **kwargs):
        """
        Logs fine-granular debugging message
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a message objects
            args: a list of positional arguments
            kwargs: a list of named arguments

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

