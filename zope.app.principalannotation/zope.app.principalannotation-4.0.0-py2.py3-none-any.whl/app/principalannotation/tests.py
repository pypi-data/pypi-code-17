##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Principal Annotation Tests

"""
import doctest
import unittest

from zope import component
from zope import interface

from zope.component.testing import PlacelessSetup

from zope.traversing.interfaces import ITraverser
from zope.container.interfaces import INameChooser

class TestImports(unittest.TestCase):


    def test_bbb_imports(self):
        # The most of functionality was moved to zope.principalannotation.
        # Let's test if old imports still work:

        from zope.app.principalannotation import interfaces as OldI
        from zope.principalannotation import interfaces as NewI
        self.assertIs(NewI.IPrincipalAnnotationUtility, OldI.IPrincipalAnnotationUtility)

        from zope.app import principalannotation as Old
        from zope.principalannotation import utility as New

        self.assertIs(Old.PrincipalAnnotationUtility, New.PrincipalAnnotationUtility)
        self.assertIs(Old.Annotations, New.Annotations)

        self.assertEqual(Old.annotations.__module__,
                         'zope.principalannotation.utility')


class TestBootstrap(PlacelessSetup, unittest.TestCase):

    def test_subscriber_utility(self):

        from zope.app.principalannotation.bootstrap import bootStrapSubscriber

        test = self

        @interface.implementer(ITraverser,
                               INameChooser)
        class SiteManager(object):

            def __init__(self):
                self._data = {}

            def traverse(self, name, request=None):
                test.assertEqual(name, 'default')
                return self

            def chooseName(self, name, utility):
                test.assertEqual(name, 'PrincipalAnnotation')
                return name

            def __getattr__(self, name):
                return getattr(component.getGlobalSiteManager(), name)

            def __setitem__(self, name, value):
                self._data[name] = value

            def __getitem__(self, name):
                return self._data[name]

            def __contains__(self, name):
                return name in self._data

        class RootFolder(dict):

            def __init__(self):
                self.sm = SiteManager()

            def getSiteManager(self):
                return self.sm

        class Connection(object):
            closed = False

            def __init__(self):
                self._root = {'Application': RootFolder()}

            def close(self):
                self.closed = True

            def root(self):
                return self._root

        class Database(object):

            def __init__(self):
                self.conn = Connection()

            def open(self):
                return self.conn

        class Event(object):

            def __init__(self):
                self.database = Database()

        event = Event()
        bootStrapSubscriber(event)

        # We closed the connection when we were done
        self.assertTrue(event.database.conn.closed)

        # We only register once
        self.assertIn('PrincipalAnnotation',
                      event.database.conn.root()['Application'].getSiteManager())

        event2 = Event()
        bootStrapSubscriber(event2)

        self.assertNotIn('PrincipalAnnotation',
                         event2.database.conn.root()['Application'].getSiteManager())


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
    ))
