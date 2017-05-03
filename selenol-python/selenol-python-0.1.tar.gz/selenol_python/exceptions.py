# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Exception declarations."""


class SelenolException(Exception):
    """Selenol abstract exception."""

    def __init__(self, message=None):
        """Constructor.

        :param message: Message to be shown to the user.
        """
        super(SelenolException, self).__init__()
        self.message = message or 'Not defined exception'

    def __str__(self):
        """Return the string describing the exception."""
        return self.message


class SelenolUnauthorizedException(SelenolException):
    """Selenol exception for unauthorized behaves."""


class SelenolWebSocketClosedException(SelenolException):
    """Selenol exception for WebSocket clossed connections."""


class SelenolMissingArgumentException(SelenolException):
    """Selenol exception for missing arguments."""

    def __init__(self, argument):
        """Constructor.

        :param argument: Name of the missing argument.
        """
        super(SelenolMissingArgumentException, self).__init__()
        self.argument = argument

    def __str__(self):
        """Return the string describing the exception."""
        return 'Argument "{0}" missing'.format(self.argument)


class SelenolMissingSessionArgumentException(SelenolException):
    """Selenol exception for missing arguments in user session."""

    def __init__(self, argument):
        """Constructor.

        :param argument: Name of the missing session argument.
        """
        super(SelenolMissingSessionArgumentException, self).__init__()

        self.argument = argument

    def __str__(self):
        """Return the string describing the exception."""
        return 'Session argument "{0}" missing'.format(self.argument)


class SelenolInvalidArgumentException(SelenolException):
    """Selenol exception for invalid arguments."""

    def __init__(self, argument, value):
        """Constructor.

        :param argument: Name of the wrong argument.
        :param value: Value of the wrong argument.
        """
        super(SelenolInvalidArgumentException, self).__init__()
        self.argument = argument
        self.value = value

    def __str__(self):
        """Return the string describing the exception."""
        return 'Argument "{0}" can not take value {1}'.format(
            self.argument, self.value)


class SelenolInvalidUserException(SelenolException):
    """Selenol exception for invalid users."""
