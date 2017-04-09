"""mod: 'hannakageul.decoder'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ('cp949', 'cp932', 'euccn','eucjp', 'i8859', 'i2022', 'utf8')


def cp949(source):
    return source.encode('iso-8859-1').decode('cp949', 'replace')


def cp932(source):
    return source.encode('iso-8859-1').decode('cp932', 'replace')


def euccn(source):
    return source.encode('iso-8859-1').decode('euc-cn', 'replace')


def eucjp(source):
    return source.encode('iso-8859-1').decode('euc-jp', 'replace')


def i8859(source):
    return source.encode('iso-8859-1').decode('iso-8859-1', 'replace')


def i2022(source):
    return source.encode('iso-8859-1').decode('iso-2022-jp', 'replace')


def utf8(source):
    return source.encode('iso-8859-1').decode('utf8', 'replace')
