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
"""Pluggable Authentication Service Tests

"""

__docformat__ = "reStructuredText"

import re
import unittest
import doctest
from zope.testing import renormalizing

import transaction
from zope.interface import directlyProvides
from zope.exceptions.interfaces import UserError

from zope.pluggableauth.factories import Principal
from zope.app.authentication.principalfolder import PrincipalFolder
from zope.app.authentication.principalfolder import IInternalPrincipal
from zope.app.authentication.testing import AppAuthenticationLayer
from zope.app.wsgi.testlayer import http

from webtest import TestApp

class FunkTest(unittest.TestCase):

    layer = AppAuthenticationLayer

    def setUp(self):
        super(FunkTest, self).setUp()
        self._testapp = TestApp(self.layer.make_wsgi_app())


    def publish(self, path, basic=None, form=None, headers=None):
        assert basic
        assert form
        self._testapp.authorization = ('Basic', tuple(basic.split(':')))

        env = {'wsgi.handleErrors': False}
        response = self._testapp.post(path, params=form,
                                      extra_environ=env, headers=headers)
        return response

    def getRootFolder(self):
        return self.layer.getRootFolder()

    def test_copypaste_duplicated_id_object(self):

        root = self.getRootFolder()

        # Create a principal Folder
        root['pf'] = PrincipalFolder()
        pf = root['pf']

        # Create a principal with p1 as login
        principal = Principal('p1')
        principal.login = 'p1'
        directlyProvides(principal, IInternalPrincipal)

        pf['p1'] = principal

        transaction.commit()
        self.assertEqual(len(pf.keys()), 1)
        #raise str([x for x in pf.keys()])

        response = self.publish('/pf/@@contents.html',
                                basic='mgr:mgrpw',
                                form={'ids:list': [u'p1'],
                                      'container_copy_button': u'Copy'})
        self.assertEqual(response.status_int, 302)


        # Try to paste the file
        with self.assertRaises(UserError) as r:
            self.publish('/pf/@@contents.html',
                         basic='mgr:mgrpw',
                         form={'container_paste_button': ''})

        e = r.exception
        self.assertIn("The given name(s)", str(e))
        self.assertIn("p1", str(e))
        self.assertIn("are already being used", str(e))

    def test_cutpaste_duplicated_id_object(self):

        root = self.getRootFolder()

        # Create a principal Folder
        root['pf'] = PrincipalFolder()
        pf = root['pf']

        # Create a principal with p1 as login
        principal = Principal('p1')
        principal.login = 'p1'
        directlyProvides(principal, IInternalPrincipal)

        pf['p1'] = principal

        transaction.commit()
        self.assertEqual(len(pf.keys()), 1)
        #raise str([x for x in pf.keys()])

        response = self.publish('/pf/@@contents.html',
                                basic='mgr:mgrpw',
                                form={'ids:list': [u'p1'],
                                      'container_cut_button': u'Cut'})
        self.assertEqual(response.status_int, 302)


        # Try to paste the file
        with self.assertRaises(UserError) as r:
            self.publish('/pf/@@contents.html',
                         basic='mgr:mgrpw',
                         form={'container_paste_button': ''})

        e = r.exception
        self.assertIn("The given name(s)", str(e))
        self.assertIn("p1", str(e))
        self.assertIn("are already being used", str(e))


checker = renormalizing.RENormalizing([
    (re.compile(r"HTTP/1\.0 200 .*"), "HTTP/1.1 200 OK"),
    (re.compile(r"HTTP/1\.0 303 .*"), "HTTP/1.1 303 See Other"),
    (re.compile(r"HTTP/1\.0 401 .*"), "HTTP/1.1 401 Unauthorized"),
    (re.compile(r"u'([^']*)'"), r"'\1'"),
])

def test_suite():
    flags = (doctest.NORMALIZE_WHITESPACE
             | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2
             | doctest.ELLIPSIS)

    def _http(query_str, *args, **kwargs):
        wsgi_app = AppAuthenticationLayer.make_wsgi_app()
        # Strip leading \n
        query_str = query_str.lstrip()
        kwargs.setdefault('handle_errors', True)
        if not isinstance(query_str, bytes):
            query_str = query_str.encode("utf-8")
        return http(wsgi_app, query_str, *args, **kwargs)

    def make_doctest(path):
        test = doctest.DocFileSuite(
            path,
            checker=checker,
            optionflags=flags,
            globs={'http': _http, 'getRootFolder': AppAuthenticationLayer.getRootFolder})
        test.layer = AppAuthenticationLayer
        return test

    principalfolder = make_doctest('../principalfolder.rst')
    groupfolder = make_doctest('../groupfolder.rst')
    pau_prefix_and_searching = make_doctest('../pau_prefix_and_searching.rst')
    group_searching_with_empty_string = make_doctest('../group_searching_with_empty_string.rst')
    special_groups = make_doctest('../special-groups.rst')
    issue663 = make_doctest('../issue663.rst')

    return unittest.TestSuite((
        principalfolder,
        groupfolder,
        pau_prefix_and_searching,
        group_searching_with_empty_string,
        special_groups,
        unittest.makeSuite(FunkTest),
        issue663,
        doctest.DocFileSuite('../schemasearch.rst'),
        ))
