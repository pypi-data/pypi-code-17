"""Base models module."""

from __future__ import absolute_import, division, print_function


class BaseExpression(object):
    """Base class for expressions."""

    def execute(self, item):
        """Execute expression.

        :param item: Item
        :type item: byte.model.Model
        """
        raise NotImplementedError


class BaseProperty(object):
    """Base class for properties."""

    def get(self, obj):
        """Get property value from object.

        :param obj: Item
        :type obj: byte.model.Model
        """
        raise NotImplementedError

    def set(self, obj, value):
        """Set property value on object.

        :param obj: Item
        :type obj: byte.model.Model

        :param value: Value
        :type value: any
        """
        raise NotImplementedError
