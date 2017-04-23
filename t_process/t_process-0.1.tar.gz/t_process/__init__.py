#!/usr/bin/env python

import errno
import os
import signal
import subprocess
import sys
import time
import timeit

def execute_command(command_list, raise_exception_on_error = False):
    '''Executes the specified command using the supplied parameters'''

    process = subprocess.Popen(command_list, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, error = process.communicate()
    status = process.returncode

    # Python3 requires the output and error to be decoded
    if sys.version_info[0] >= 3:
        output = output.decode('utf-8')
        error = error.decode('utf-8')

    if (status and raise_exception_on_error):
        raise RuntimeError('Status: {0}{1}Output: {2}{1}Error: {3}'.format(status, os.linesep, output, error))

    return status, output, error

def kill_process(pid, wait_timeout_ms = 5000, force_kill_after_timeout = False):
    '''Kills the specified process forcefully if it does not exit within the allowable timeout'''

    # First send the SIGTERM to the process and return fast if the pid does not exist
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError as ex:
        if ex.errno == errno.ESRCH:
            return
        else:
            raise

    # Now wait for the process to exit within the specified timeout
    if wait_timeout_ms <= 0:
        return
    start_time = timeit.default_timer()
    while True:
        time.sleep(0.05)
        try:
            os.kill(pid, 0)
        except OSError as ex:
            if ex.errno == errno.ESRCH:
                return
        current_time = timeit.default_timer()
        elapsed_time = (current_time - start_time) * 1000
        if elapsed_time >= wait_timeout_ms:
            if force_kill_after_timeout:
                break
            else:
                raise IOError('Elapsed time {0} ms exceeded specified timeout {1} ms while waiting for process with pid {2} to exit'.format(elapsed_time, wait_timeout_ms, pid))

    # If specified, force kill the process now after waiting for the specified timeout
    try:
        os.kill(pid, signal.SIGKILL)
    except OSError as sk_ex:
        if ex.errno == errno.ESRCH:
            return
        else:
            raise
