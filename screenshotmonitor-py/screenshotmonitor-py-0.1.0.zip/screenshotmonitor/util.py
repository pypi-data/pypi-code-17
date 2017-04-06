# -*- coding: utf-8 -*-
"""

"""

from datetime import datetime
import re

_FIRST_CAP_REGEX = re.compile('(.)([A-Z][a-z]+)')
_ALL_CAP_REGEX = re.compile('([a-z0-9])([A-Z])')


def camelcase_to_underscored(chars):
    """
    Converts camelCase strings to not_camel_cased strings.

    Credit to: http://stackoverflow.com/a/1176023

    :param chars: the camelCase to be converted
    :return: the given string with underscores instead
    """
    s1 = _FIRST_CAP_REGEX.sub(r'\1_\2', chars)
    return _ALL_CAP_REGEX.sub(r'\1_\2', s1).lower()


def convert_timestamp_to_date(seconds):
    """
    Silently converts an integer to a datetime object. Any exceptions are quietly ignore and the original value
    is returned.

    :param seconds: the number of seconds since the epoch
    :return: either the original value given or a datetime object
    """
    try:
        seconds = datetime.utcfromtimestamp(int(seconds))
    except TypeError:
        pass  # wasn't an int
    return seconds


def underscore_dict_keys(d):
    """
    Given a dictionary, converts camelCase keys to non_camel_case keys.

    :param d: the source dictionary
    :return: a new dictionary with underscored keys and no camelCase keys
    """
    d = d.copy()

    keys = []
    for k in d.keys():
        conv = camelcase_to_underscored(k)
        if k != conv:
            keys.append((conv, k))

    for conv, k in keys:
        d[conv] = d.pop(k)

    return d
