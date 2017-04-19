# -*- coding: utf-8 -*-
from .exceptions import InvalidJaeumError, InvalidHangulError
from .internals import count_jamos, inject_jaeum
from .internals import is_jaeum, is_hangul


def replace_eumjul(target, index, replacement):
    """Recreate the unicode string with new Eumjul.

    :param target: a single or series of Hangul.
    :type target: unicode
    :type index: int
    :param index: an index to use the given replacement.
    :param replacement: an Eumjul to use as an replacement.
    :type replacement: unicode
    :return: new unicode with the replacement.
    :rtype: unicode
    """
    buff = []
    for i, c in enumerate(target):
        if i == index:
            buff.append(replacement)
        else:
            buff.append(c)
    return u''.join(buff)


def get_complexity(target):
    """Get a list of complexities for each syllable.

    :param target: a single or series of Hangul.
    :type target: unicode
    :return: a list of Jamo counts for the given unicode string.
    :rtype: list
    """
    return map(count_jamos, target)


def get_indices_by_complexity(target, complexity):
    """Get a list of indices for the complexity.

    :param target: a single or series of Hangul to compute complexity on.
    :type target: unicode
    :param complexity: level of complexity to look for.
    :type complexity: int
    :return: a filtered list of indices for the given complexity.
    :rtype: list
    """
    complexities = get_complexity(target) # [3, 2, 2, 1, 3]
    return map(lambda p: p[0], filter(lambda (i, c): c == complexity, enumerate(complexities)))


def verify_jaeum(u):
    """Verify the given unicode as Jaeum.

    :param u: a unicode string that should represent Jaeum.
    :raise: exceptions.InvalidJaeumError
    :return: the given unicode.
    :rtype: boolean
    """
    if is_jaeum(u):
        return u
    raise InvalidJaeumError


def verify_hangul(u):
    """Verify the given unicode as Hangul.

    :param u: a unicode string that should represent Hangul.
    :raise: exceptions.InvalidHangulError
    :return: the given unicode.
    :rtype: boolean
    """
    if is_hangul(u):
        return u
    raise InvalidHangulError
