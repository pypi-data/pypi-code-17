# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


class TrytonException(Exception):
    pass


class UserError(TrytonException):

    def __init__(self, message, description=''):
        super(UserError, self).__init__('UserError', (message, description))
        self.message = message
        self.description = description
        self.code = 1


class UserWarning(TrytonException):

    def __init__(self, name, message, description=''):
        super(UserWarning, self).__init__('UserWarning', (name, message,
                description))
        self.name = name
        self.message = message
        self.description = description
        self.code = 2


class LoginException(TrytonException):
    """Request the named parameter for the login process.
    The type can be 'password' or 'char'.
    """

    def __init__(self, name, message, type='password'):
        super(LoginException, self).__init__(
            'LoginException', (name, message, type))
        self.name = name
        self.message = message
        self.type = type
        self.code = 3


class ConcurrencyException(TrytonException):

    def __init__(self, message):
        super(ConcurrencyException, self).__init__('ConcurrencyException',
            message)
        self.message = message
        self.code = 4
