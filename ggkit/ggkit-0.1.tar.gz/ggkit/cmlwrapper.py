#!/usr/bin/env python
# coding=utf-8
#
# cmlwrapper.py:
#
# Copyright (c) 2017 gogleyin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import time
from subprocess import Popen, PIPE
import threading
import logging
logger = logging.getLogger(__name__ if __name__ != '__main__' else os.path.splitext(os.path.basename(__file__))[0])
logger.setLevel(logging.DEBUG)


class CmlWrapper(object):
    """
    Remained Issue:
    Example:
        cmd = 'pinga www.baidu.com'
        clt = CmlWrapper(cmd)
        ret = clt.wait()
        logger.debug('wait return: %s return code: %s' % (ret, clt.returncode))
    In this example, both ret and clt.returncode will be unstable, could be either 127 or 0.
    """
    # todo I find an issue that with outupt=True, _subprocess.wait()'s returning value will be unstable.
    def __init__(self, cmd, output=True):
        self._cmd = cmd
        logger.debug('$ {0}'.format(self._cmd))
        self._subprocess = Popen(self._cmd, shell=True, stderr=PIPE, stdout=PIPE)
        if output:
            self.print_stdout(block=False)
            self.print_stderr(block=False)

    def terminate(self):
        if self.is_running and self._subprocess:
            return self._subprocess.terminate()

    @property
    def returncode(self):
        if not self._subprocess:
            logger.debug('self._subprocess is None.')
            return
        return self._subprocess.returncode

    def wait(self):
        if not self._subprocess:
            logger.debug('Subprocess has not been created yet.')
            return
        try:
            ret = self._subprocess.wait()
            logger.debug('Subprocess did finished with exit code: %s' % ret)
            return ret
        except KeyboardInterrupt:
            logger.debug('Receive KeyboardInterrupt.')
            self.terminate()
            time.sleep(0.1)  # Termination will cost some time. Without this waiting, ReturnCode will be None
            return self._subprocess.returncode

    def stdout_lines(self):
        """ blocking """
        if not self.is_running:
            logger.warning('Subprocess not running!')
            return
        while self.is_running:
            try:
                yield self._subprocess.stdout.readline()
            except KeyboardInterrupt:
                logger.debug('Receive KeyboardInterrupt.')
                self.terminate()

    def stderr_lines(self):
        """ blocking """
        if not self.is_running:
            logger.warning('Subprocess not running!')
            return
        while self.is_running:
            try:
                yield self._subprocess.stderr.readline()
            except KeyboardInterrupt:
                logger.debug('Receive KeyboardInterrupt.')
                self.terminate()

    def _print_stdout(self, log_level=logging.DEBUG):
        while self.is_running:
            try:
                line = self.stdout_lines().next()
                if line:
                    logger.log(log_level, line.strip())
            except StopIteration:
                break
        logger.debug('PrintStdout will exit.')

    def _print_stderr(self, log_level=logging.ERROR):
        while self.is_running:
            try:
                line = self.stderr_lines().next()
                if line:
                    logger.log(log_level, line.strip())
            except StopIteration:
                break
        logger.debug('PrintStderr will exit.')

    def print_stdout(self, block=True, log_level=logging.DEBUG):
        if not self._subprocess or not self.is_running:
            return
        if block:
            return self._print_stdout()
        thread = threading.Thread(target=self._print_stdout, name='PrintStdout', args=(log_level,))
        thread.setDaemon(True)
        thread.start()

    def print_stderr(self, block=True, log_level=logging.ERROR):
        if not self._subprocess or not self.is_running:
            return
        if block:
            return self._print_stderr()
        thread = threading.Thread(target=self._print_stderr, name='PrintStderr', args=(log_level,))
        thread.setDaemon(True)
        thread.start()

    @property
    def is_running(self):
        if not self._subprocess:
            return False
        return self._subprocess.poll() is None


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cmd = 'ping www.google.com'
    clt = CmlWrapper(cmd)
    ret = clt.wait()
    logger.debug('wait return: %s return code: %s' % (ret, clt.returncode))

