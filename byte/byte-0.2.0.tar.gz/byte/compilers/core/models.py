"""Compiler models module."""

from __future__ import absolute_import, division, print_function


class Operation(object):
    """Base operation class."""

    pass


class DeleteOperation(Operation):
    """Delete operation class."""

    pass


class InsertOperation(Operation):
    """Insert operation class."""

    def __init__(self, items):
        """Create insert operation.

        :param items: Items to insert
        :type items: list of dict
        """
        self.items = items


class SelectOperation(Operation):
    """Select operation class."""

    def __init__(self, where):
        """Create select operation.

        :param where: Where expressions
        :type where: list
        """
        self.where = where


class UpdateOperation(Operation):
    """Update operation class."""

    pass
