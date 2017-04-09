"""mod: 'hannakageul.converter.eucjp'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

shift-jis based function
"""

from hannakageul import decoder
from hannakageul import encoder


__all__ = ('euccn', 'eucjp', 'euckr', 'jis', 'utf8')


def euccn(source):
    """Convert shift-jis string to euc-cn"""
    result = decoder.euccn(encoder.cp932(source))
    return result


def eucjp(source):
    """Convert shift-jis string to euc-jp"""
    result = decoder.eucjp(encoder.cp932(source))
    return result


def euckr(source):
    """Convert shift-jis string to cp949"""
    result = decoder.cp949(encoder.cp932(source))
    return result


def jis(source):
    """Convert shift-jis string to jis(iso-2022-jp)"""
    result = decoder.i2022(encoder.cp932(source))
    return result


def utf8(source):
    """Convert shift-jis string to utf8"""
    result = decoder.utf8(encoder.cp932(source))
    return result
