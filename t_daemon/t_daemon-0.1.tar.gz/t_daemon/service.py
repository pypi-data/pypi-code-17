#!/usr/bin/env python

import errno
import os
import sys
import time

import t_io
import t_process

class Service:

    '''
    A service daemon implmentation that can be inherited to provide linux daemon functionality.

    A subclass need only override the execute() method
    '''

    @staticmethod
    def __delete_pid_file(pid_file):
        '''Deletes the corresponding daemon pid file
           Method exists so that it can be registered atexit'''

        try:
            os.remove(pid_file)
        except OSError as ex:
            if ex.errno != errno.ENOENT:
                raise

    @staticmethod
    def __read_pid_file(pid_file):
        '''Reads the corresponding daemon pid file'''

        try:
            pid = t_io.read_file(pid_file)
            pid = int(pid.strip())
        except IOError as ex:
            if ex.errno == errno.ENOENT:
                pid = None
            else:
                raise

        return pid

    # Public Methods

    @staticmethod
    def start(lambda_returns_daemon, pid_file):
        '''Starts the daemon implementation'''
        pid = Service.__read_pid_file(pid_file)
        if pid:
            raise RuntimeError('pid_file {0} exists with pid {1}; daemon is currently running...'.format(pid_file, pid))
        else:
            daemon = lambda_returns_daemon()
            if daemon.daemonize():
                daemon.execute()
            # else the original root parent process will simply return

    @staticmethod
    def stop(pid_file):
        '''Stops the daemon implementation'''
        pid = Service.__read_pid_file(pid_file)
        if not pid:
            raise RuntimeError('pid_file {0} does not exist; daemon is not currently running...'.format(pid_file))
        else:
            t_process.kill_process(pid, force_kill_after_timeout = True)
            Service.__delete_pid_file(pid_file)

    @staticmethod
    def restart(lambda_returns_daemon, pid_file):
        '''Restarts the daemon implementation'''
        Service.stop(pid_file)
        Service.start(lambda_returns_daemon, pid_file)
