# -*- coding: utf-8 -*-
"""
jaeum_modifier.api
~~~~~~~~~~~~~~~~~~

This module implements the API for jaeum_modifier.

:copyright: (c) 2017 by Hyunchel Kim.
:license: MIT, see LICENSE for more dtails.
"""


from .exceptions import NoIndexFoundError, NoComplexityFoundError
from .utils import (
    get_indices_by_complexity, inject_jaeum,
    replace_eumjul, verify_jaeum
)


def modify(target, index, jaeum):
    """Modify target on index by injecting jaeum.

    :param target: a word or sentence composed in Hangul.
    :param index: desired index to perform Jaeum injection on.
    :param jaeum: a unicode string that should represent Jaeum.
    :raise: exceptions.NoIndexFoundError
    :return: new unicode string in Hangul with a Jaeum replaced at the specified index.
    :rtype: unicode
    """
    if index < 0:
        index = len(target) + index
    if index >= len(target) or index < 0:
        raise NoIndexFoundError('desired index exceeds the range')
    verified_jaeum = verify_jaeum(jaeum)
    return replace_eumjul(target, index, inject_jaeum(target[index], verified_jaeum))


def modify_all(target, jaeum):
    """Modify all jaeums in the given target to the given jaeum.

    :param target: a word or sentence composed in Hangul.
    :param jaeum: a unicode string that should represent Jaeum.
    :return: new unicode string in Hangul with a Jaeum injected.
    :rtype: unicode
    """
    verified_jaeum = verify_jaeum(jaeum)
    for index, _ in enumerate(target):
        # TODO: I don't like the re-assignment
        target = replace_eumjul(target, index, inject_jaeum(target[index], verified_jaeum))
    return target


# TODO: include how many to set
def modify_by_complexity(target, jaeum, complexity):
    """Set jaeum by complexity.

    :param target: a word or sentence composed in Hangul.
    :param jaeum: a unicode string that should represent Jaeum.
    :param complexity: desired complexity to perform Jaeum injections on.
    :raise: exceptions.NoComplexityFoundError
    :return: new unicode string in Hangul with Jaeum(s) replaced.
    :rtype: unicode
    """
    indices = get_indices_by_complexity(target, complexity)
    if not indices:
        raise NoComplexityFoundError('there is no eumjul with the desired complexity')
    for index in indices:
        verified_jaeum = verify_jaeum(jaeum)
        # TODO: I don't like the re-assignment
        target = replace_eumjul(target, index, inject_jaeum(target[index], verified_jaeum))
    return target
