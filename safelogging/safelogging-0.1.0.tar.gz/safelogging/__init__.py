"""
This module contains some additional logging functionality on top of the
standard python logging library that could be useful for applications.
"""

import os
import sys
import socket
import logging

from logging.handlers import SysLogHandler


class ResilientSysLogHandler(SysLogHandler):
    """
    A resilient syslog handler class which extends on the official python
    syslog handler class with the extension of file stream logging fallback
    mechanism when connection to the syslog server is lost.

    Optional init keyword argument ``fallback_stream`` can be specified to
    override the default stream ``sys.stderr``.
    """

    def __init__(self, *args, **kwargs):
        self.app_name = get_app_name()
        self.fallback = False
        self.fallback_stream = kwargs.pop('fallback_stream', sys.stderr)
        try:
            SysLogHandler.__init__(self, *args, **kwargs)
        except socket.error:
            self.fallback = True
            self._fallback_logging(
                "Unable to connect to syslog. "
                "Falling back to file stream logging")

    def emit(self, record):
        try:
            SysLogHandler.emit(self, record)
            if self.fallback:
                self._fallback_logging(
                    "Connection to syslog re-established. "
                    "Will do logging there from now on")
                self.fallback = False
        except ResilientSysLogHandler.FallbackException:
            pass

    def handleError(self, record):
        if not self.fallback:
            self._fallback_logging(
                "Connection to syslog broken. "
                "Falling back to file stream logging")
            self.fallback = True
        self._fallback_logging(record)
        raise ResilientSysLogHandler.FallbackException

    def _fallback_logging(self, record):
        if not self.fallback_stream:
            return
        if isinstance(record, logging.LogRecord):
            message = self.format(record)
        else:
            message = record
        try:
            self.fallback_stream.write("[%s] %s\n" % (self.app_name, message))
        except IOError:
            pass

    class FallbackException(Exception):
        """
        Private exception definition for determining when an emitted log
        message have used the fallback logging mechanism.
        """
        pass


class LoggerFile(object):
    """
    A class that emulates a file object that forwards any lines of text written
    to it to a logger.

    Example:

        >>> sys.stdout = LoggerFile("my_app")
        >>> sys.stderr = LoggerFile("my_app", logging.ERROR)
    """

    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.level = level
        self.buffer = ""

    def write(self, data):
        self.buffer += data
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            self.logger.log(self.level, line)

    def flush(self):
        if self.buffer:
            self.logger.log(self.level, self.buffer)
            self.buffer = ""


def get_app_name():
    """
    Convenience function for getting the name of the running application with
    special handling if application is a runit service.
    """
    path = os.path.realpath(sys.argv[0])
    name = os.path.basename(path)
    if name != "run":
        return name
    return os.path.basename(os.path.dirname(path))
