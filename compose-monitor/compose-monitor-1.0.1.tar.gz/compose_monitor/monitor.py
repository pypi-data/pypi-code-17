import time
import logging
import traceback

from compose.cli import command
from compose.config.errors import ConfigurationError

import logger

from cStringIO import StringIO
import sys


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class Monitor(object):
    def __init__(self, path, options, filelog=None):
        global log

        if "log" not in globals():
            if filelog is not None:
                log = logging.getLogger(__name__)
                log.addHandler(logger.FileHandler(filelog))
                log.setLevel(logging.DEBUG)
            else:
                log = logging.getLogger(__name__)
                log.addHandler(logger.StreamHandler())
                log.setLevel(logging.DEBUG)

        self.path = path
        self.options = options
        try:
            self.project = command.project_from_options(self.path,
                                                        self.options)
        except ConfigurationError:
            log.error("Can't create a monitor unit\n{}".
                format(traceback.format_exc()))
            raise SystemExit

    def run(self, timeout):
        log.info("Monitor started successfully")
        while True:
            try:
                with Capturing() as output:
                    for service in self.project.services:
                        service.pull()
                self.project.up()
            except Exception:
                log.error("Service checking failed\n{}".
                    format(traceback.format_exc()))

            log.info("Checked successfully\n{}".format(output))
            time.sleep(timeout)
