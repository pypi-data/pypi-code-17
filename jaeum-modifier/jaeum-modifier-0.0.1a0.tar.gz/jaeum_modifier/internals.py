# -*- coding: utf-8 -*-
"""
jaeum_modifier.internals
~~~~~~~~~~~~~~~~~~~~~~~~

This module implements internal utilities that utilizes third party library(Hangulize).
"""


from hangulize.hangul import join, split, Jaeum
from hangulize.hangul import isJaeum, ishangul
from hangulize.hangul import Null as NULL


def count_jamos(eumjul):
    """Returns a number of jamos this syllable contains.

    Examples:
        Syllable u'안' contains three jamos(u'ㅇ', u'ㅏ', u'ㄴ').
        Syllable u'아' contains two jamos(u'ㅇ', u'ㅏ', u'').

    :param eumjul: a single syllable of Hangul.
    :return: a number of total Jamos that is used to complete the given Eumjul(syllable).
    :rtype: int
    """
    return len(filter(lambda jamo: jamo != NULL, split(eumjul)))


def inject_jaeum(eumjul, jaeum):
    """Inject the given Jaeum to the given Eumjul.

    :param eumjul: a single syllable of Hangul.
    :param jaeum: a single Jamo to inject.
    :return: new Eumjul created with the given Jaeum injected.
    :rtype: unicode
    """
    jamos = split(eumjul)
    return join((jaeum, jamos[1], jamos[2]))


def is_jaeum(jaeum):
    """Test if the given unicode is Jaeum.

    :param u: a unicode string that should represent Jaeum.
    :return: result of this test.
    :rtype: boolean
    """
    return isJaeum(jaeum)


def is_hangul(hangul):
    """Test if the given unicode is Hangul.

    :param u: a unicode string that should represent Hangul.
    :return: result of this test.
    :rtype: boolean
    """
    return ishangul(hangul)
