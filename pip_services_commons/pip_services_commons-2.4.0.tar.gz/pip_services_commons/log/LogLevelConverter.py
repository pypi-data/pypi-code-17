# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.LogLevelConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log level converter implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .LogLevel import LogLevel

class LogLevelConverter(object):
    
    @staticmethod
    def to_log_level(value):
        """
        Converts object to log level

        Args:
            value: an object to be converted

        Returns: log level
        """
        if value == None:
            return LogLevel.Info

        value = str(value).upper()
        if ("0" == value) or ("NOTHING" == value) or ("NONE" == value):
            return LogLevel.None
        elif ("1" == value) or ("FATAL" == value):
            return LogLevel.Fatal
        elif ("2" == value) or ("ERROR" == value):
            return LogLevel.Error
        elif ("3" == value) or ("WARN" == value) or ("WARNING" == value):
            return LogLevel.Warn
        elif ("4" == value) or ("INFO" == value):
            return LogLevel.Info
        elif ("5" == value) or ("DEBUG" == value):
            return LogLevel.Debug
        elif ("6" == value) or ("TRACE" == value):
            return LogLevel.Trace
        else:
            return LogLevel.Info

    @staticmethod
    def to_string(level):
        """
        Converts log level into string representation

        Args:
            level: level to be converted

        Returns: a string representation of the log level
        """
        if level == LogLevel.Fatal:
            return "FATAL" 
        if level == LogLevel.Error:
            return "ERROR" 
        if level == LogLevel.Warn:
            return "WARN" 
        if level == LogLevel.Info:
            return "INFO" 
        if level == LogLevel.Debug:
            return "DEBUG" 
        if level == LogLevel.Trace:
            return "TRACE"
        return "UNDEF"

    @staticmethod
    def to_integer(level):
        """
        Converts log level into integer representation

        Args:
            level: level to be converted

        Returns: an integer representation of the log level
        """
        if level == LogLevel.Fatal:
            return 1 
        if level == LogLevel.Error:
            return 2 
        if level == LogLevel.Warn:
            return 3 
        if level == LogLevel.Info:
            return 4 
        if level == LogLevel.Debug:
            return 5 
        if level == LogLevel.Trace:
            return 6
        return 0

