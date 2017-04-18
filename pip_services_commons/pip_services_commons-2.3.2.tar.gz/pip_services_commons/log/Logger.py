# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.Logger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .LogLevel import LogLevel
from .ILogger import ILogger
from .LogLevelConverter import LogLevelConverter
from ..config.IReconfigurable import IReconfigurable

class Logger(object, ILogger, IReconfigurable):

    _level = LogLevel.Info

    def configure(self, config):
        self._level = LogLevelConverter.to_log_level(config.get_as_object("level"))

    def get_level(self):
        return self._level

    def set_level(self, level):
        self._level = level

    def _write(self, level, correlation_id, error, message):
        raise NotImplementedError('Method from abstract implementation')

    def _format_and_write(self, level, correlation_id, error, message, *args, **kwargs):
        if message != None and len(message) > 0 and len(kwargs) > 0:
            message = message.format(*args, **kwargs)
        self._write(level, correlation_id, error, message)

    def log(self, level, correlation_id, error, message, *args, **kwargs):
        self._format_and_write(level, correlation_id, error, message, args, kwargs)

    def fatal(self, correlation_id, error, message, *args, **kwargs):
        self._format_and_write(LogLevel.Fatal, correlation_id, error, message, args, kwargs)

    def error(self, correlation_id, error, message, *args, **kwargs):
        self._format_and_write(LogLevel.Error, correlation_id, error, message, args, kwargs)

    def warn(self, correlation_id, message, *args, **kwargs):
        self._format_and_write(LogLevel.Warn, correlation_id, None, message, args, kwargs)

    def info(self, correlation_id, message, *args, **kwargs):
        self._format_and_write(LogLevel.Info, correlation_id, None, message, args, kwargs)

    def debug(self, correlation_id, message, *args, **kwargs):
        self._format_and_write(LogLevel.Debug, correlation_id, None, message, args, kwargs)

    def trace(self, correlation_id, message, *args, **kwargs):
        self._format_and_write(LogLevel.Trace, correlation_id, None, message, args, kwargs)

