"""mod: 'hannakageul.converter.eucjp'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

euc-jp based function
"""

from hannakageul import decoder
from hannakageul import encoder


__all__ = ('euccn', 'euckr', 'jis', 'sjis', 'utf8')


def euccn(source):
    """Convert euc-jp string to euc-cn"""
    result = decoder.euccn(encoder.eucjp(source))
    return result


def euckr(source):
    """Convert euc-jp string to cp949"""
    result = decoder.cp949(encoder.eucjp(source))
    return result


def jis(source):
    """Convert euc-jp string to jis(iso-2022-jp)"""
    result = decoder.i2022(encoder.eucjp(source))
    return result


def sjis(source):
    """Convert euc-jp string to shift-jis"""
    result = decoder.cp932(encoder.eucjp(source))
    return result


def utf8(source):
    """Convert euc-jp string to utf-8"""
    result = decoder.utf8(encoder.eucjp(source))
    return result
