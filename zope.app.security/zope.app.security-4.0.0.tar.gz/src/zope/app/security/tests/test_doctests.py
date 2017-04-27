import unittest
import doctest

from zope.app.wsgi.testlayer import BrowserLayer
import zope.app.security


PermissionsLayer = BrowserLayer(zope.app.security.tests)

def test_suite():
    suite = doctest.DocFileSuite('persistentlist.rst')
    suite.layer = PermissionsLayer
    return unittest.TestSuite([suite])
