"""mod: 'hannakageul.converter.eucjp'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

jis based function
"""

from hannakageul import decoder
from hannakageul import encoder


__all__ = ('euccn', 'eucjp', 'euckr', 'sjis', 'utf8')


def euccn(source):
    """Convert jis(iso-2022-jp) string to euc-cn"""
    result = decoder.euccn(encoder.i2022(source))
    return result


def eucjp(source):
    """Convert jis(iso-2022-jp) string to euc-jp"""
    result = decoder.eucjp(encoder.i2022(source))
    return result


def euckr(source):
    """Convert jis(iso-2022-jp) string to cp949"""
    result = decoder.cp949(encoder.i2022(source))
    return result


def sjis(source):
    """Convert jis(iso-2022-jp) string to shift-jis"""
    result = decoder.cp932(encoder.i2022(source))
    return result


def utf8(source):
    """Convert cp949 string to utf-8"""
    result = decoder.utf8(encoder.i2022(source))
    return result
