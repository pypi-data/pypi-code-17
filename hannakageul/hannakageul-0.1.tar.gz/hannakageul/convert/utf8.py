"""mod: 'hannakageul.converter.utf8'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

utf8 based function
"""

from hannakageul import decoder
from hannakageul import encoder


__all__ = ('euccn', 'eucjp', 'euckr', 'jis', 'sjis')


def euccn(source):
    """Convert utf-8 string to euc-cn"""
    result = decoder.euccn(encoder.utf8(source))
    return result


def eucjp(source):
    """Convert utf-8 string to euc-jp"""
    result = decoder.eucjp(encoder.utf8(source))
    return result


def euckr(source):
    """Convert utf-8 string to cp949"""
    result = decoder.cp949(encoder.utf8(source))
    return result


def jis(source):
    """Convert utf-8 string to jis(iso-2022-jp)"""
    result = decoder.i2022(encoder.utf8(source))
    return result


def sjis(source):
    """Convert utf-8 string to shift-jis"""
    result = decoder.cp932(encoder.utf8(source))
    return result
