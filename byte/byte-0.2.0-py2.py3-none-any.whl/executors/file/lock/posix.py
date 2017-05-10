"""File executor posix lock."""

from __future__ import absolute_import, division, print_function

from byte.executors.file.lock.base import BaseFileLock, FileLockError

import fcntl


class BasePosixFileLock(BaseFileLock):
    """Base posix lock class."""

    def release(self):
        """Release lock."""
        # Unlock file
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_UN)
        except Exception as ex:
            raise FileLockError(ex)


class PosixExclusiveFileLock(BasePosixFileLock):
    """Exclusive posix lock class."""

    def acquire(self, blocking=None):
        """Acquire lock.

        :param blocking: Block until the lock has been acquired
        :type blocking: bool
        """
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = fcntl.LOCK_EX

        if not blocking:
            mode |= fcntl.LOCK_NB

        # Lock file
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_EX)
        except Exception as ex:
            raise FileLockError(ex)


class PosixSharedFileLock(BasePosixFileLock):
    """Shared posix lock class."""

    def acquire(self, blocking=None):
        """Acquire lock.

        :param blocking: Block until the lock has been acquired
        :type blocking: bool
        """
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = fcntl.LOCK_SH

        if not blocking:
            mode |= fcntl.LOCK_NB

        # Lock file
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_SH)
        except Exception as ex:
            raise FileLockError(ex)
