# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.NullLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .LogLevel import LogLevel
from .ILogger import ILogger

class NullLogger(object, ILogger):

    def get_level(self):
        return LogLevel.Nothing

    def set_level(self, level):
        pass

    def log(self, level, correlation_id, error, message, *args, **kwargs):
        pass

    def fatal(self, correlation_id, error, message, *args, **kwargs):
        pass

    def error(self, correlation_id, error, message, *args, **kwargs):
        pass

    def warn(self, correlation_id, message, *args, **kwargs):
        pass

    def info(self, correlation_id, message, *args, **kwargs):
        pass

    def debug(self, correlation_id, message, *args, **kwargs):
        pass

    def trace(self, correlation_id, message, *args, **kwargs):
        pass

