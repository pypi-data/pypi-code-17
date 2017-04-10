#!/usr/bin/env python3

"""
 Not really a CherryPy tool, but additional
 session storage method injected to cherrypy.
 Reminder: it is Linux only compatible
"""

import fcntl
import os
import time
from contextlib import contextmanager

import cherrypy
from cherrypy.lib import sessions


class GtfileSession(sessions.FileSession):

    """Replacement of FileSession that uses fcntl locks."""

    _locks = {}

    @contextmanager
    def open(self, mode='r'):
        """ Open session for reading or writing depending on mode parameter."""
        path = self._get_file_path()
        self.acquire_lock(path)
        # needed when nesting of 'r' mode context in 'w' one
        self.load(path)
        yield self
        if mode is 'w':
            self.loaded = True  # force write (flag could be lost by nesting)
            self.save()
        else:
            self.loaded = False  # bummer, better way needs to be implemented
        self.release_lock(path)

    def load(self, path=None):  # pylint: disable=arguments-differ
        """Copy stored session data into this session instance."""
        data = self._load(path)
        # data is either None or a tuple (session_data, None)
        mtime = os.stat(path).st_mtime
        if data is None or mtime < (time.time()-self.timeout*60):
            if self.debug:
                cherrypy.log('Expired session %r, flushing data.' % self.id,
                             'TOOLS.SESSIONS')
            self._data = {}
        else:
            if self.debug:
                cherrypy.log('Data loaded for session %r.' % self.id,
                             'TOOLS.SESSIONS')
            os.utime(path)
            self._data = data[0]
        self.loaded = True

        # Stick the clean_thread in the class, not the instance.
        # The instances are created and destroyed per-request.
        cls = self.__class__
        if self.clean_freq and not cls.clean_thread:
            # clean_up is an instancemethod and not a classmethod,
            # so that tool config can be accessed inside the method.
            t = cherrypy.process.plugins.Monitor(
                cherrypy.engine, self.clean_up, self.clean_freq * 60,
                name='Session cleanup')
            t.subscribe()
            cls.clean_thread = t
            t.start()
            if self.debug:
                cherrypy.log('Started cleanup thread.', 'TOOLS.SESSIONS')

    def save(self):
        """Save session data."""
        # custom implementation that doesn't release lock implicitly
        # so context manager (especially nested) doesn't cause exceptions

        # If session data has never been loaded then it's never been
        #   accessed: no need to save it
        if self.loaded:
            # None given as expiration time, as it's not used by this implementation:
            self._save(None)
            self.loaded = False

    def acquire_lock(self, path=None):

        """Acquire an exclusive lock on the currently-loaded session data."""
        if path is None:
            path = self._get_file_path()

        if path in self._locks and self.locked:
            self._locks[path][1] += 1
            return
        pathfd = open(path, 'a+')
        if not fcntl.flock(pathfd, fcntl.LOCK_EX):
            self._locks[path] = [pathfd, 1]
            self.locked = True

    def release_lock(self, path=None):  # pylint: disable=arguments-differ
        """Release the lock on the currently-loaded session data."""

        if path is None:
            path = self._get_file_path()

        if path in self._locks and \
           self._locks[path][1] > 1 and self.locked:
            self._locks[path][1] -= 1
            return

        self.locked = False
        # closing file handle removes exclusive lock
        self._locks.pop(path)[0].close()

sessions.GtfileSession = GtfileSession
