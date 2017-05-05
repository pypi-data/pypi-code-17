##############################################################################
#
# Copyright (c) 2004-2007 Zope Corporation and Contributors.
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
"""Functional tests for zope.app.catalog


"""
import doctest
import unittest
import re

from zope.testing import renormalizing

from zope.app.catalog.testing import AppCatalogLayer

from zope.app.wsgi.testlayer import http as _http


def http(query_str, *args, **kwargs):
    wsgi_app = AppCatalogLayer.make_wsgi_app()
    # Strip leading \n
    query_str = query_str.lstrip()
    kwargs.setdefault('handle_errors', False)
    if not isinstance(query_str, bytes):
        query_str = query_str.encode("utf-8")
    return _http(wsgi_app, query_str, *args, **kwargs)



def test_suite():
    checker = renormalizing.RENormalizing((
        (re.compile("HTTP/1.0"), "HTTP/1.1"),
        (re.compile(r"u('[^']*')"), r"\1"),
    ))

    suite = doctest.DocFileSuite(
        'README.rst',
        globs={'http': http, 'getRootFolder': AppCatalogLayer.getRootFolder},
        checker=checker,
        optionflags=(doctest.ELLIPSIS
                     | doctest.NORMALIZE_WHITESPACE
                     | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2),
    )
    suite.layer = AppCatalogLayer
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
