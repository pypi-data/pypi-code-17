import doctest
import unittest

from zope.component import testing
from zope.app.schema.vocabulary import _clear

def setUp(test):
    testing.setUp()
    _clear()

def tearDown(test):
    testing.tearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
                     setUp=setUp, tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))
