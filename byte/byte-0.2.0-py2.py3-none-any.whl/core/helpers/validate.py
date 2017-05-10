"""Validation helper functions module."""

from __future__ import absolute_import, division, print_function


def is_list_of(items, value_type):
    """Validate list :code:`items` match :code:`value_type`.

    :param items: Items
    :type items: list

    :param value_type: Value type
    :type value_type: class
    """
    if not isinstance(items, list):
        return False

    def match():
        for item in items:
            if type(value_type) is tuple:
                yield is_tuple_of(item, value_type)
                continue

            yield isinstance(item, value_type)

    return all(match())


def is_tuple_of(items, value_type):
    """Validate tuple :code:`items` match :code:`value_type`.

    :param items: Items
    :type items: tuple

    :param value_type: Value type
    :type value_type: class
    """
    if not isinstance(items, tuple):
        return False

    def match():
        yield len(items) == len(value_type)

        for x, item in enumerate(items):
            if type(value_type) is tuple:
                yield isinstance(item, value_type[x])
                continue

            yield isinstance(item, value_type)

    return all(match())
