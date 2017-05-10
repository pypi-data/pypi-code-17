"""Statement base module."""

from __future__ import absolute_import, division, print_function

import functools


class Statement(object):
    """Statement class."""

    def __init__(self, collection, model, state=None):
        """Create statement.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type: model: class

        :param state: Initial state
        :type state: dict or None
        """
        self.collection = collection
        self.model = model

        self.state = state or {}

        self._result = None

    def clone(self):
        """Clone statement.

        :rtype: Statement
        """
        def copy(value):
            if type(value) is dict:
                return value.copy()

            if type(value) is list:
                return list(value)

            if type(value) is tuple:
                return tuple(value)

            return value

        return self.__class__(
            self.collection, self.model,
            state=copy(self.state)
        )

    def execute(self):
        """Execute statement."""
        return self.collection.execute(self)

    def filter(self, *args, **kwargs):
        """Filter statement results."""
        raise NotImplementedError

    def first(self):
        """Execute statement, and return the first item from the result."""
        with self.execute() as result:
            for item in result:
                return item

        return None

    def __enter__(self):
        """Enter statement context."""
        self._result = self.execute()

        return self._result

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit statement context (release resources)."""
        if self._result is None:
            return

        self._result.close()


def operation(func):
    """Statement operation decorator.

    Clones the query before calling the bound method.
    """
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        if not hasattr(self, 'clone'):
            raise ValueError('Class \'%s\' has no "clone" method defined' % (self.__class__.__name__,))

        # Clone existing query
        query = self.clone()

        # Execute operation, and return new query
        func(query, *args, **kwargs)
        return query

    return inner
