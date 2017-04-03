# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Module `murdock.logger`
-----------------------

A logger interface based on the `logging` module (standard lib).

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import socket
import sys
import time


class Logger(object):
    """Configuration class for logging with the logging module.
    """

    def __init__(
            self, name=None, filename=None, logdir='.',
            file_level=logging.INFO, console_level=None, group='docking'):
        if name is not None:
            self.logger = logging.getLogger(name)
        else:
            self.logger = logging.getLogger()
        if filename is None and console_level is None:
            self.logger.addHandler(logging.NullHandler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.logger = self
        self.ch = None
        self.fh = None
        self.name = name
        self.group = group
        self.logdir = logdir
        self.filename = filename
        if filename is not None:
            self.add_file_handler(file_level)
        if console_level is not None:
            self.add_console_handler(console_level)

    def add_console_handler(self, level):
        """Add console handler to the logger.
        """
        self.ch = logging.StreamHandler(sys.stdout)
        self.ch.setLevel(level)
        f = self._custom_formatter_console()
        f.formatTime = custom_formatTime_console
        self.ch.setFormatter(f)
        self.logger.addHandler(self.ch)
        return True

    def add_file_handler(self, level):
        """Add file handler to the logger.
        """
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        filepath = os.path.join(os.path.abspath(self.logdir), self.filename)
        self.fh = logging.FileHandler(filepath, encoding='UTF-8')
        self.fh.setLevel(level)
        f = self._custom_formatter_file()
        f.formatTime = custom_formatTime_file
        self.fh.setFormatter(f)
        self.logger.addHandler(self.fh)
        return True

    def _custom_formatter_console(self):
        fmt = '{filename} %(asctime)s %(levelname)8s %(message)s'
        return logging.Formatter(
            fmt=fmt.format(filename='[%s]' % self.filename))

    def _custom_formatter_file(self):
        fmt = '[{hostname}:%(process)d] %(asctime)s %(levelname)8s %(message)s'
        return logging.Formatter(fmt=fmt.format(hostname=socket.gethostname()))


def custom_formatTime_console(record, datefmt=None):
    """Customize timing output for a console log record.

    Overrides a `logging.Formatter.formatTime` method in order to customize
    timing output for a log record. The string returned will appear in the
    output exactly where `%(asctime)s` is placed in the log format string.

    """
    return time.strftime('%H:%M:%S', time.localtime())



def custom_formatTime_file(record, datefmt=None):
    """Customize timing output for a file log record.

    Overrides a `logging.Formatter.formatTime` method in order to customize
    timing output for a log record. The string returned will appear in the
    output exactly where `%(asctime)s` is placed in the log format string.

    """
    return time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
