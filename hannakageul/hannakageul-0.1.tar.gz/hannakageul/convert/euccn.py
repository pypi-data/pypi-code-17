"""mod: 'hannakageul.converter.euccn'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

euc-cn based function
"""

from hannakageul import decoder
from hannakageul import encoder


__all__ = ('eucjp', 'euckr', 'jis', 'sjis', 'utf8')


def eucjp(source):
    """Convert euc-cn string to cp949"""
    result = decoder.eucjp(encoder.euccn(source))
    return result


def euckr(source):
    """Convert euc-cn string to cp949"""
    result = decoder.cp949(encoder.euccn(source))
    return result


def jis(source):
    """Convert euc-cn string to jis(iso-2022-jp)"""
    result = decoder.i2022(encoder.euccn(source))
    return result


def sjis(source):
    """Convert euc-cn string to shift-jis"""
    result = decoder.cp932(encoder.euccn(source))
    return result


def utf8(source):
    """Convert euc-cn string to utf-8"""
    result = decoder.utf8(encoder.euccn(source))
    return result
