##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
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

import unittest

if str is bytes:
    from io import BytesIO as StringIO
else:
    from io import StringIO


from ZODB.MappingStorage import MappingStorage
from ZODB.DB import DB
from zope.testing import cleanup
from zope.app.debug.debug import Debugger

from zope.configuration import xmlconfig

from zope.component.testlayer import ZCMLFileLayer
from zope.security.management import endInteraction

import zope.app.debug.tests

DebugLayer = ZCMLFileLayer(zope.app.debug.tests)

class FolderView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return u"Hi"

class TestDebugger(unittest.TestCase):

    layer = DebugLayer

    def setUp(self):
        endInteraction()
        self.storage = MappingStorage()
        self.db = DB(self.storage)

    def test_from_database(self):
        dbg = Debugger.fromDatabase(self.db)
        self.assertIs(self.db, dbg.db)

    def test_construct(self):
        self.assertRaises(IOError, Debugger)
        dbg = Debugger(self.db)
        self.assertIs(self.db, dbg.db)

    def test_root(self):
        # Only happens from the constructor
        dbg = Debugger.fromDatabase(self.db)
        self.assertRaises(KeyError, dbg.root)
        dbg = Debugger(self.db)
        self.assertIsNotNone(dbg.root())

    def test_debug(self):
        out = StringIO()
        dbg = Debugger(self.db, stdout=out)

        class Pdb(object):

            def __init__(self):
                self.breaks = set()
                self.calls = []
                self.s = []
                self.c = []

            def set_break(self, filename, lineno):
                self.breaks.add(filename)

            def runcall(self, *args):
                self.calls.append(args)

            def do_s(self, arg):
                self.s.append(arg)

            def do_c(self, arg):
                self.c.append(arg)


        dbg.Pdb = Pdb

        pdb = dbg.debug()

        self.assertIn('to jump to published object call',
                      out.getvalue())
        self.assertEqual(1, len(pdb.breaks))
        self.assertEqual(1, len(pdb.calls))

        out.seek(0)

        pdb.do_ob('')
        self.assertNotIn('already done', out.getvalue())
        self.assertEqual(['', ''], pdb.s)
        self.assertEqual(['', ''], pdb.c)

        pdb.do_pub('')
        self.assertIn('pub already done', out.getvalue())

        pdb.do_ob('')
        self.assertIn('ob already done', out.getvalue())

    def test_run(self):
        dbg = Debugger(self.db)
        time, clock, status = dbg.run()
        self.assertGreaterEqual(time, 0)
        self.assertGreaterEqual(clock, 0)
        self.assertEqual(200, status)

    def test_publish(self):
        stdout = StringIO()
        dbg = Debugger(self.db, stdout=stdout)
        time, clock, status = dbg.publish()
        self.assertGreaterEqual(time, 0)
        self.assertGreaterEqual(clock, 0)
        self.assertEqual(200, status)

        self.assertIn('Content-Type', stdout.getvalue())

    def test_request(self):
        dbg = Debugger(self.db)
        # One query string
        req = dbg._request(path='/?q=1')

        # Too many query strings
        self.assertEqual(req['QUERY_STRING'], 'q=1')
        self.assertRaises(ValueError, dbg._request, path="/?q=1?q=2")

        # Environment
        req = dbg._request(environment={'k': 42})
        self.assertEqual(req['k'], 42)

        req = dbg._request(basic="foo:bar")
        self.assertFalse(req.has_key('HTTP_AUTHORIZATION'))
        self.assertEqual(req._auth, 'Basic Zm9vOmJhcg==')

        # Form
        req = dbg._request(form={'k': 42})
        self.assertEqual(req.form['k'], 42)

        # Request factory

        class Request(object):
            pub = None
            def __init__(self, *args):
                pass

            def setPublication(self, p):
                self.pub = p

        req = dbg._request(request=Request)
        self.assertIsInstance(req, Request)
        self.assertIsNotNone(req.pub)

        # Body data
        req = dbg._request(stdin=u'unicode\nlines')
        self.assertEqual(req.bodyStream.readlines(),
                         [b'unicode\n', b'lines'])
        req = dbg._request(stdin=b'bytes\nlines')
        self.assertEqual(req.bodyStream.readlines(),
                         [b'bytes\n', b'lines'])

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
