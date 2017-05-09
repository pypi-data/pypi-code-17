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
"""Generation-browser tests

"""
import re
import unittest
import doctest
import importlib
from webtest import TestApp
from zope import component as ztapi
from zope.testing import renormalizing
from zope.app.generations.testing import GenerationsLayer
from zope.generations.generations import SchemaManager, generations_key
from zope.generations.interfaces import ISchemaManager

class TestDatabaseSchema(unittest.TestCase):

    layer = GenerationsLayer

    def setUp(self):
        self._testapp = TestApp(self.layer.make_wsgi_app())

    def commit(self):
        import transaction
        transaction.commit()

    def publish(self, path, basic=None, headers=None):
        assert basic
        self._testapp.authorization = ('Basic', tuple(basic.split(':')))
        env = {'wsgi.handleErrors': False}
        response = self._testapp.get(path, extra_environ=env, headers=headers)
        return response

    def test(self):
        root = self.layer.getRootFolder()._p_jar.root()
        appkey = 'zope.generations.demo'
        root[generations_key][appkey] = 0
        self.commit()
        manager = SchemaManager(0, 3, 'zope.generations.demo')

        ztapi.provideUtility(manager, ISchemaManager, appkey)
        sm = ztapi.getSiteManager()
        self.addCleanup(sm.unregisterUtility, manager, ISchemaManager, appkey)

        response = self.publish('/++etc++process/@@generations.html',
                                basic='globalmgr:globalmgrpw')
        body = response.text
        body = u' '.join(body.split())
        expect = (u'zope.generations.demo</a> </td> '
                  u'<td>0</td> <td>3</td> <td>0</td> '
                  u'<td> <input type="submit" value=" evolve " '
                  u'name="evolve-app-zope.generations.demo"> </td>')
        self.assertIn(expect, body)

        response = self.publish('/++etc++process/@@generations.html'
                                '?evolve-app-zope.generations.demo=evolve',
                                basic='globalmgr:globalmgrpw')
        body = response.text
        body = u' '.join(body.split())
        expect = (u'zope.generations.demo</a> </td> '
                  u'<td>0</td> <td>3</td> <td>1</td> '
                  u'<td> <input type="submit" value=" evolve " '
                  u'name="evolve-app-zope.generations.demo"> </td>')
        self.assertIn(expect, body)

        response = self.publish('/++etc++process/@@generations.html'
                                '?evolve-app-zope.generations.demo=evolve',
                                basic='globalmgr:globalmgrpw')
        body = response.text
        body = u' '.join(body.split())
        expect = (u'zope.generations.demo</a> </td> '
                  u'<td>0</td> <td>3</td> <td>2</td> '
                  u'<td> <input type="submit" value=" evolve " '
                  u'name="evolve-app-zope.generations.demo"> </td>')
        self.assertIn(expect, body)

        response = self.publish('/++etc++process/@@generations.html'
                                '?evolve-app-zope.generations.demo=evolve',
                                basic='globalmgr:globalmgrpw')
        body = response.text
        body = u' '.join(body.split())
        expect = (u'zope.generations.demo</a> </td> '
                  u'<td>0</td> <td>3</td> <td>3</td> '
                  u'<td> <span>')
        self.assertIn(expect, body)


def _make_import_test(mod_name, attrname):
    def test(self):
        mod = importlib.import_module('zope.app.generations.' + mod_name)
        self.assertIsNotNone(getattr(mod, attrname))

    return test

class TestBWCImports(unittest.TestCase):

    for mod_name, attrname in (('generations', 'ISchemaManager'),
                               ('utility', 'getRootFolder'),
                               ('interfaces', 'ISchemaManager')):
        locals()['test_' + mod_name] = _make_import_test(mod_name, attrname)



def test_suite():
    checker = renormalizing.RENormalizing((
        (re.compile(r"u('.*')"), r"\1"),
    ))
    return unittest.TestSuite((
        doctest.DocTestSuite(
            'zope.app.generations.browser.managers',
            checker=checker),
        doctest.DocTestSuite(
            'zope.app.generations.browser.managerdetails',
            checker=checker),
        unittest.defaultTestLoader.loadTestsFromName(__name__),
    ))
