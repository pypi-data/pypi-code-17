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

"""Selenol service datastructures implementation."""

from .exceptions import (SelenolMissingArgumentException,
                         SelenolMissingSessionArgumentException)


class SelenolDictionary(object):
    """Selenol dictionary."""

    def __init__(self, dictionary, exception=SelenolMissingArgumentException):
        """Constructor.

        :param dictionary: Mapping container.
        :param exception: Exception to be raised in case of unexisting key.
        """
        self.dictionary = dictionary
        self.exception = exception

    def __getitem__(self, key):
        """Return the item in the given key or raise and exception.

        :param key: Key that holds the desired value.
        """
        if key not in self.dictionary:
            raise self.exception(key)

        result = self.dictionary[key]

        if isinstance(result, list):
            return SelenolList(result, self.exception)
        elif isinstance(result, dict):
            return SelenolDictionary(result, self.exception)
        else:
            return result


class SelenolList(object):
    """Selenol list."""

    def __init__(self, items, exception=IndexError):
        """Constructor.

        :param items: Sequence of elements.
        :param exception: Exception to be raised in case of wrong position.
        """
        self.items = items
        self.exception = exception

    def __getitem__(self, pos):
        """Return the item at the fiven position or raise an exception.

        :param pos: Index position of the desired value.
        """
        if not isinstance(pos, int) or pos < 0 or pos >= len(self.items):
            raise self.exception(pos)

        result = self.items[pos]

        if isinstance(result, list):
            return SelenolList(result, self.exception)
        elif isinstance(result, dict):
            return SelenolDictionary(result, self.exception)
        else:
            return result


class SelenolMessage(object):
    """Selenol message."""

    def __init__(self, message):
        """Selenol message constructor.

        :param message: Dictionary with keys content, session and request_id.
        """
        self.session = SelenolDictionary(
            message['content'].get('session', {}),
            SelenolMissingSessionArgumentException)
        self.content = SelenolDictionary(message['content'].get('content', {}))
        self.request_id = message['request_id']
