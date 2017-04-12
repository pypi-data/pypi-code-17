# -*- coding: utf-8 -*-
"""
    pip_services_commons.log.LogLevel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log level enumeration
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class LogLevel(object):
    """
    Logging levels to determine details of logged messages
    """

    Nothing = 0
    """
    Nothing to be logged
    """

    Fatal = 1
    """
    Logs only fatal errors that cause microservice to fail
    """

    Error = 2
    """
    Logs all errors - fatal or recoverable
    """

    Warn = 3
    """
    Logs errors and warnings
    """

    Info = 4
    """
    Logs errors and important information messages
    """

    Debug = 5
    """
    Logs everything up to high-level debugging information
    """

    Trace = 6
    """
    Logs everything down to fine-granular debugging messages
    """
