#!/usr/bin/env python

import atexit
import errno
import logging
import os
import sys
import time

import t_io
import t_logging

class Daemon:

    '''
    A service daemon implmentation that can be inherited to provide linux daemon functionality.

    A subclass need only override the execute() method
    '''

    def __init__(self, pid_file, log_level = logging.INFO, std_in = '/dev/null', std_out = '/dev/null', std_err = '/dev/null'):
        '''Initialize class with the requisite pid file path and I/O descriptors'''

        self.logger = t_logging.get_logger(log_level)

        self.logger.info('Daemon instance initializing...')

        self.pid_file = pid_file

        self.std_in = std_in
        self.std_out = std_out
        self.std_err = std_err

        self.logger.info('Daemon instance initialized.')

    # Private Methods

    def __write_pid_file(self, pid_file):
        '''Writes the executing process' pid to file'''

        self.logger.info('Writing executing daemon process id from file {0}...'.format(pid_file))

        pid = os.getpid()
        t_io.write_file_x(pid_file, str(pid))

        self.logger.info('Wrote executing daemon process id {0}.'.format(pid))

    def __delete_pid_file(self):
        '''Deletes the corresponding daemon pid file
           Method exists so that it can be registered atexit'''

        self.logger.info('Deleting daemon pid file {0}...'.format(self.pid_file))

        try:
            os.remove(self.pid_file)
            self.logger.info('Deleted daemon pid file')
        except OSError as ex:
            if ex.errno != errno.ENOENT:
                raise
            else:
                self.logger.info('Daemon pid file does not exist')

    def __daemonize_fork(self):
        '''Forks the executing process daemon style'''

        self.logger.info('Forking process...')

        # Forks the process daemon style (parent exits; child continues)
        # 0 is returned as the fork result within the child process
        # The pid of the child process is returned as the fork result within the parent process
        returned_pid = os.fork()
        if returned_pid != 0:
            self.logger.info('Continueing parent process {0}.'.format(os.getpid()))
        else:
            self.logger.info('Continueing child process {0} execution...'.format(os.getpid()))

        return returned_pid

    # Public Methods

    def get_pid_file(self):
        '''Returns the associated daemon pid file path'''
        return self.pid_file

    def daemonize(self):
        '''Daemonizes the executing process via standard double forking procedures'''

        # Fork the process for the first time
        if self.__daemonize_fork() != 0:
            # Have the parent immediately return
            return False

        # Detach from parent process settings in child
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # Fork the process for the second time
        if self.__daemonize_fork() != 0:
            self.logger.info('Exiting parent process (which is a child of the root parent process).')
            sys.exit(0);

        # Redirect IO file descriptors
        sys.stdin.flush()
        sys.stdout.flush()
        sys.stderr.flush()
        std_in = open(self.std_in, 'r')
        std_out = open(self.std_out, 'a+')
        std_err = open(self.std_err, 'a+')
        os.dup2(std_in.fileno(), sys.stdin.fileno())
        os.dup2(std_out.fileno(), sys.stdout.fileno())
        os.dup2(std_err.fileno(), sys.stderr.fileno())

        # Write daemon pid to file and setup file deletion on exit
        self.__write_pid_file(self.pid_file)
        atexit.register(self.__delete_pid_file)

        return True

    def execute(self):
        '''Daemon service implementation logic that should be overriden by the subclass'''
        raise NotImplementedError('Method should be overriden in subclass implementation')
