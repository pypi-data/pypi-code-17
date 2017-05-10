"""File executor lock package."""

from __future__ import absolute_import, division, print_function

__all__ = (
    'ExclusiveFileLock',
    'SharedFileLock'
)

try:
    from byte.executors.file.lock.posix import (
        PosixExclusiveFileLock as ExclusiveFileLock,
        PosixSharedFileLock as SharedFileLock
    )
except ImportError:
    try:
        from byte.executors.file.lock.win32 import (
            Win32ExclusiveFileLock as ExclusiveFileLock,
            Win32SharedFileLock as SharedFileLock
        )
    except ImportError:
        try:
            from byte.executors.file.lock.msvcrt import (
                MsvcrtExclusiveFileLock as ExclusiveFileLock,
                MsvcrtSharedFileLock as SharedFileLock
            )
        except ImportError:
            ExclusiveFileLock = None
            SharedFileLock = None
