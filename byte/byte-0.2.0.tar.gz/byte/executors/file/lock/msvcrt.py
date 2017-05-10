"""File executor Visual C++ runtime lock."""

from __future__ import absolute_import, division, print_function

from byte.executors.file.lock.base import BaseFileLock, FileLockError

import msvcrt
import os
import six

if six.PY2:
    def is_file(value):
        """Retrieve boolean indicating the provided :code:`value` is a file.

        :param value: Value
        :type value: any
        """
        return type(value) is file
else:
    import io

    def is_file(value):
        """Retrieve boolean indicating the provided :code:`value` is a file.

        :param value: Value
        :type value: any
        """
        return isinstance(value, io.IOBase)


class BaseMsvcrtFileLock(BaseFileLock):
    """Base Visual C++ runtime lock class."""

    def release(self):
        """Release lock."""
        try:
            # Save current position, and seek to the start
            if is_file(self.fp):
                fn = self.fp.fileno()
                pos = self.fp.tell()

                self.fp.seek(0)
            else:
                fn = self.fp
                pos = os.lseek(fn, 0, 0)

                os.lseek(fn, 0, 0)

            # Unlock file
            try:
                msvcrt.locking(fn, msvcrt.LK_UNLCK, -1)
            finally:
                # Seek back to original position
                os.lseek(fn, pos, 0)
        except Exception as ex:
            raise FileLockError(ex)


class MsvcrtExclusiveFileLock(BaseMsvcrtFileLock):
    """Exclusive Visual C++ runtime lock class."""

    def acquire(self, blocking=None):
        """Acquire lock.

        :param blocking: Block until the lock has been acquired
        :type blocking: bool
        """
        if blocking is None:
            blocking = self.blocking

        try:
            # Save current position, and seek to the start
            if is_file(self.fp):
                fn = self.fp.fileno()
                pos = self.fp.tell()

                self.fp.seek(0)
            else:
                fn = self.fp
                pos = os.lseek(fn, 0, 0)

                os.lseek(fn, 0, 0)

            # Unlock file
            try:
                msvcrt.locking(fn, msvcrt.LK_LOCK if blocking else msvcrt.NBLCK, -1)
            finally:
                # Seek back to original position
                os.lseek(fn, pos, 0)
        except Exception as ex:
            raise FileLockError(ex)


class MsvcrtSharedFileLock(BaseMsvcrtFileLock):
    """Shared Visual C++ runtime lock class."""

    def acquire(self, blocking=None):
        """Acquire lock.

        :param blocking: Block until the lock has been acquired
        :type blocking: bool
        """
        if blocking is None:
            blocking = self.blocking

        try:
            # Save current position, and seek to the start
            if is_file(self.fp):
                fn = self.fp.fileno()
                pos = self.fp.tell()

                self.fp.seek(0)
            else:
                fn = self.fp
                pos = os.lseek(fn, 0, 0)

                os.lseek(fn, 0, 0)

            # Unlock file
            try:
                msvcrt.locking(fn, msvcrt.LK_RLCK if blocking else msvcrt.NBRLCK, -1)
            finally:
                # Seek back to original position
                os.lseek(fn, pos, 0)
        except Exception as ex:
            raise FileLockError(ex)
