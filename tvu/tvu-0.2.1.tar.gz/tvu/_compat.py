import sys

if sys.version_info < (3,):
    text = unicode
    basestr = basestring
else:
    text = str
    basestr = str
