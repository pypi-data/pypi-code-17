# -*- coding: utf-8 -*-
"""
    pip_services_container.ProcessContainer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Process container implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import os
import sys
import signal
import time
import threading

from pip_services_commons.log import ConsoleLogger
from pip_services_commons.config import ConfigParams
from .Container import Container

class ProcessContainer(Container):
    _config_path = './config/config.yaml'
    _exit_event = None

    def __init__(self, name = None, description = None):
        super(ProcessContainer, self).__init__(name, description)
        self._logger = ConsoleLogger()
        self._exit_event = threading.Event()

    def _get_config_path(self):
        args = sys.argv
        index = 0
        while index < len(args):
            arg = args[index]
            next_arg = args[index + 1] if index < len(args) - 1 else None
            next_arg = None if next_arg != None and next_arg.startswith('-') else next_arg;
            if next_arg != None:
                if arg == "--config" or arg == "-c":
                    return next_arg
            index += 1
        return self._config_path

    def _get_parameters(self):
        # Process command line parameters
        args = sys.argv
        line = ''
        index = 0
        while index < len(args):
            arg = args[index]
            next_arg = args[index + 1] if index < len(args) - 1 else None
            next_arg = None if next_arg != None and next_arg.startswith('-') else next_arg;
            if next_arg != None:
                if arg == "--param" or arg == "--params" or arg == "-p":
                    if len(line) > 0:
                        line = line + ';'
                    line = line + next_arg
                    index += 1
            index += 1

        parameters = ConfigParams.from_string(line)

        # Process environmental variables
        for (k, v) in os.environ.items():
            parameters[k] = v

        return parameters


    def _show_help(self):
        args = sys.argv
        index = 0
        while index < len(args):
            arg = args[index]
            if arg == "--help" or arg == "-h":
                return True
            index += 1
        return False


    def _print_help():
        print("Pip.Services process container - http://www.github.com/pip-services/pip-services")
        print("run [-h] [-c <config file>] [-p <param>=<value>]*")


    def _capture_errors(self, correlation_id):
        def handle_exception(exc_type, exc_value, exc_traceback):
            self._logger.fatal(correlation_id, exc_value, "Process is terminated")
            self._exit_event.set()
            #sys.exit(1)

        sys.excepthook = handle_exception

    def _capture_exit(self, correlation_id):
        self._logger.info(correlation_id, "Press Control-C to stop the microservice...")

        def sigint_handler(signum, frame):
            self._logger.info(correlation_id, "Goodbye!")
            self._exit_event.set()
            #sys.exit(1)
            
        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)

        # Wait and close
        self._exit_event.clear()
        while not self._exit_event.is_set():
            try:
                self._exit_event.wait(1)
            except:
                pass # Do nothing...

    def run(self):
        if self._show_help():
            self._print_help()
            return

        correlation_id = self._info.name
        path = self._get_config_path()
        parameters = self._get_parameters()
        self.read_config_from_file(correlation_id, path, parameters)

        self._capture_errors(correlation_id)
        self.open(correlation_id)
        self._capture_exit(correlation_id)
        self.close(correlation_id)
