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
"""Functional tests for NotFoundError
"""
import doctest
import unittest
from zope.component.interfaces import ComponentLookupError
from zope.app.exception.testing import AppExceptionLayer
from zope.app.exception.browser.tests import BrowserTestCase
from zope.app.wsgi.testlayer import http

class RaiseError(object):

    def __call__(self):
        raise Exception()


class RaiseComponentLookupError(object):

    def __call__(self):
        raise ComponentLookupError()


class TestComponentLookupError(BrowserTestCase):

    layer = AppExceptionLayer

    def testComponentLookupError(self):
        response = self.publish('/foobar', basic='mgr:mgrpw',
                                handle_errors=True)
        self.assertEqual(response.status_int, 404)
        body = response.unicode_normal_body
        self.assertIn(
            'The page that you are trying to access is not available', body)

class TestMisc(unittest.TestCase):

    def test_user(self):
        from zope.app.exception.browser import user
        view = user.UserErrorView()
        view.context = self
        self.assertEqual(view.title(), self.__class__.__name__)

    def test_interfaces(self):
        from zope.app.exception import interfaces
        from zope.browser.interfaces import ISystemErrorView
        self.assertEqual(interfaces.ISystemErrorView, ISystemErrorView)

def test_suite():
    TestComponentLookupError.layer = AppExceptionLayer

    def _http(query_str, *args, **kwargs):
        wsgi_app = AppExceptionLayer.make_wsgi_app()
        # Strip leading \n
        query_str = query_str.lstrip()
        kwargs.setdefault('handle_errors', True)
        if not isinstance(query_str, bytes):
            query_str = query_str.encode("utf-8")
        return http(wsgi_app, query_str, *args, **kwargs)


    systemerror = doctest.DocFileSuite(
        '../systemerror.rst',
        optionflags=doctest.ELLIPSIS,
        globs={'http': _http})

    systemerror.layer = AppExceptionLayer
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        systemerror,
    ))
