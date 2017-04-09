# -*- coding: utf-8 -*-
"""
    pip_services_container.ProcessContainer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Process container implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import sys
import signal
import time
import threading

from pip_services_commons.log import ConsoleLogger
from .Container import Container

class ProcessContainer(Container):
    _exit_event = None

    def __init__(self):
        super(ProcessContainer, self).__init__()
        self._logger = ConsoleLogger()
        self._exit_event = threading.Event()

    def read_config_from_args_or_file(self, correlation_id, default_path):
        args = sys.argv
        config_path = args[1] if len(args) > 1 else default_path
        self.read_config_from_file(correlation_id, config_path)

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

    def run(self, correlation_id):
        self._capture_errors(correlation_id)
        self.start(correlation_id)
        self._capture_exit(correlation_id)
        self.stop(correlation_id)

    def run_with_config(self, correlation_id, config):
        self.set_config(config)
        self.run(correlation_id)

    def run_with_config_file(self, correlation_id, path):
        self.read_config_from_file(correlation_id, path)
        self.run(correlation_id)

    def run_with_config_from_args_or_file(self, correlation_id, default_path):
        self.read_config_from_args_or_file(correlation_id, default_path)
        self.run(correlation_id)
