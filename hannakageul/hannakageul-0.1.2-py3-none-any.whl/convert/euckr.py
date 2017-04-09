"""mod: 'hannakageul.converter.eucjp'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

euc-kr based function
"""

from hannakageul import decoder
from hannakageul import encoder


__all__ = ('euccn', 'eucjp', 'jis', 'sjis', 'utf8')


def euccn(source):
    """Convert cp949 string to euc-cn"""
    result = decoder.euccn(encoder.cp949(source))
    return result


def eucjp(source):
    """Convert cp949 string to euc-jp"""
    result = decoder.eucjp(encoder.cp949(source))
    return result


def jis(source):
    """Convert cp949 string to jis(iso-2022-jp)"""
    result = decoder.i2022(encoder.cp949(source))
    return result


def sjis(source):
    """Convert cp949 string to shift-jis"""
    result = decoder.cp932(encoder.cp949(source))
    return result


def utf8(source):
    """Convert cp949 string to utf-8"""
    result = decoder.utf8(encoder.cp949(source))
    return result
