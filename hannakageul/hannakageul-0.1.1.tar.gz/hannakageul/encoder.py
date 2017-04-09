"""mod: 'hannakageul.encoder'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ('cp949', 'cp932', 'euccn','eucjp', 'i2022', 'utf8')


def cp949(source):
    return source.encode('cp949', 'replace').decode('iso-8859-1')


def cp932(source):
    return source.encode('cp932', 'replace').decode('iso-8859-1')


def euccn(source):
    return source.encode('euc-cn', 'replace').decode('iso-8859-1')


def eucjp(source):
    return source.encode('euc-jp', 'replace').decode('iso-8859-1')


def i2022(source):
    return source.encode('iso-2022-jp', 'replace').decode('iso-8859-1')


def utf8(source):
    return source.encode('utf8', 'replace').decode('iso-8859-1')
