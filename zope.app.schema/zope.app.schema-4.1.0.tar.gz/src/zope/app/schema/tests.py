import doctest
import unittest

from zope.testing import cleanup

def setUp(_test):
    cleanup.setUp()

def tearDown(_test):
    cleanup.tearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.rst',
                     setUp=setUp, tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))
