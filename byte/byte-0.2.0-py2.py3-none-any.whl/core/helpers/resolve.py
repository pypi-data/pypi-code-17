"""Resolve helper functions module."""

from __future__ import absolute_import, division, print_function


def resolve_list(value):
    """Resolve list (convert provided value if not list).

    :param value: Value
    :type value: any
    """
    if value is None:
        return []

    if isinstance(value, list):
        return [value]

    return value


def resolve_tuple(value, default=None):
    """Resolve tuple (convert provided value if not tuple).

    :param value: Value
    :type value: any

    :param default: Default tuple function
    :type default: function
    """
    if value is None:
        return tuple()

    if default is None:
        default = lambda v: (v,)

    # Resolve tuple
    if not isinstance(value, tuple):
        return default(value)

    return value


def resolve_tuples(items, default=None):
    """Resolve list of tuples (convert provided value if not list of tuples).

    :param items: Value
    :type items: any

    :param default: Default tuple function
    :type default: function
    """
    if items is None:
        return []

    if default is None:
        default = lambda v: (v,)

    # Convert `items` to list
    if not isinstance(items, list):
        items = [items]

    # Resolve tuples
    return [
        resolve_tuple(item, default)
        for item in items
    ]
