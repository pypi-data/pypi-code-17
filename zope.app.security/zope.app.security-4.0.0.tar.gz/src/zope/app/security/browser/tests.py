##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Security Views Tests

"""
__docformat__ = "reStructuredText"
import unittest
import doctest

from zope.app.security.tests.test_doctests import PermissionsLayer

class TestBWCImports(unittest.TestCase):

    def test_principalterms_imports(self):
          import zope.app.security.browser.principalterms as old
          import zope.authentication.principal as new

          self.assertIs(old.PrincipalTerms, new.PrincipalTerms)
          self.assertIs(old.Term, new.PrincipalTerm)

    def test_settings_imports(self):
        import zope.app.security.settings as old
        import zope.securitypolicy.settings as new

        self.assertIs(old.Allow, new.Allow)

    def test_protectclass_imports(self):
        import zope.app.security.protectclass as old
        import zope.security.checker as new1
        import zope.security.protectclass as new2

        self.assertIs(old.Checker, new1.Checker)
        self.assertIs(old.protectName, new2.protectName)

    def test__protections(self):
        import zope.app.security._protections as new

        new.protect()

def test_suite():
    def make_doctest(path):
        test = doctest.DocFileSuite(path)
        test.layer = PermissionsLayer
        return test

    search = make_doctest('authutilitysearchview.rst')

    login = make_doctest('loginlogout.rst')

    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        search,
        login
    ))
