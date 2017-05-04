"""Online CA server package.

Contrail Project
"""
__author__ = "P J Kershaw"
__date__ = "23/03/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__license__ = """BSD - See LICENSE file in top-level directory"""
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import six

# For Python 3 convert ASCII strings to unicode, for Python 2 pass through
if six.PY2:
    unicode_for_py3 = lambda string_: string_
else:
    unicode_for_py3 = lambda string_: (hasattr(string_, 'decode') and
                                       string_.decode() or string_)

# String conversion utility for Python 3
if six.PY3:
    _string2bytes = lambda string_: bytes(string_, 'utf-8')
    _bytes2string = lambda bytes_: bytes_.decode(encoding='utf-8')
else:
    _string2bytes = lambda string_: bytes(string_)
    _bytes2string = lambda bytes_: bytes_
