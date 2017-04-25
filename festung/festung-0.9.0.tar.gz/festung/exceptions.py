from __future__ import absolute_import

import exceptions


class Error(exceptions.StandardError):

    def __init__(self, message, errors=None):
        super(Error, self).__init__(message)
        self.errors = errors


class Warning(exceptions.StandardError):
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class InternalError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class DataError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass
