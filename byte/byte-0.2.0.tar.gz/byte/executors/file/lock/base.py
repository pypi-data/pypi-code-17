"""File executor base lock module."""

from __future__ import absolute_import, division, print_function


class BaseFileLock(object):
    """Base file lock class."""

    def __init__(self, fp, blocking=True):
        """Create file lock.

        :param fp: File
        :type fp: file or io.IOBase

        :param blocking: Default blocking mode
        :type blocking: bool
        """
        self.fp = fp

        self.blocking = blocking

    def acquire(self, blocking=None):
        """Acquire lock.

        :param blocking: Block until the lock has been acquired
        :type blocking: bool
        """
        raise NotImplementedError

    def release(self):
        """Release lock."""
        raise NotImplementedError

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class FileLockError(Exception):
    """File lock error class."""

    pass
