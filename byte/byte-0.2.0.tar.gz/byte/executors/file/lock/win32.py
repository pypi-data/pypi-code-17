"""File executor win32 lock module."""

from __future__ import absolute_import, division, print_function

from byte.executors.file.lock.base import BaseFileLock, FileLockError

import pywintypes
import win32con
import win32file


class BaseWin32FileLock(BaseFileLock):
    """Base win32 lock class."""

    def __init__(self, fp):
        """Create win32 lock.

        :param fp: File
        :type fp: file or io.IOBase
        """
        super(BaseWin32FileLock, self).__init__(fp)

        # Retrieve win32 file handle
        self.handle = win32file._get_osfhandle(self.fp.fileno())

    def release(self):
        """Release lock."""
        # Unlock file
        try:
            win32file.UnlockFileEx(self.handle, 0, 0x7fff0000, pywintypes.OVERLAPPED())
        except Exception as ex:
            raise FileLockError(ex)


class Win32ExclusiveFileLock(BaseWin32FileLock):
    """Exclusive win32 lock class."""

    def acquire(self, blocking=None):
        """Acquire lock.

        :param blocking: Block until the lock has been acquired
        :type blocking: bool
        """
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = win32con.LOCKFILE_EXCLUSIVE_LOCK

        if not blocking:
            mode += win32con.LOCKFILE_FAIL_IMMEDIATELY

        # Lock file
        try:
            win32file.LockFileEx(self.handle, mode, 0, 0x7fff0000, pywintypes.OVERLAPPED())
        except Exception as ex:
            raise FileLockError(ex)


class Win32SharedFileLock(BaseWin32FileLock):
    """Shared win32 lock class."""

    def acquire(self, blocking=None):
        """Acquire lock.

        :param blocking: Block until the lock has been acquired
        :type blocking: bool
        """
        if blocking is None:
            blocking = self.blocking

        # Determine lock mode
        mode = 0

        if not blocking:
            mode += win32con.LOCKFILE_FAIL_IMMEDIATELY

        # Lock file
        try:
            win32file.LockFileEx(self.handle, mode, 0, 0x7fff0000, pywintypes.OVERLAPPED())
        except Exception as ex:
            raise FileLockError(ex)
