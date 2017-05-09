#############################################################################
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

import importlib
import unittest

from zope.testing import cleanup

def _make_import_test(mod_name, attrname):
    def test(self):
        mod = importlib.import_module('zope.app.folder.' + mod_name)
        self.assertIsNotNone(getattr(mod, attrname))

    return test

class TestBWCImports(unittest.TestCase):

    for mod_name, attrname in (('interfaces', 'IFolder'),
                               ('folder', 'Folder'),
                               ('filerepresentation', 'RootDirectoryFactory'),
    ):
        locals()['test_' + mod_name] = _make_import_test(mod_name, attrname)

class TestConfiguration(cleanup.CleanUp,
                        unittest.TestCase):

    def test_root_configuration(self):
        from zope.configuration import xmlconfig

        xmlconfig.string("""
        <configure xmlns="http://namespaces.zope.org/zope"
          xmlns:browser="http://namespaces.zope.org/browser"
          i18n_domain="zope">
          <include package="zope.browsermenu" file="meta.zcml"/>
          <include package="zope.browserpage" file="meta.zcml"/>
          <!-- These normally come from zope.app.zcmlfiles/menus.zcml -->
          <browser:menu
           id="zmi_views"
           title="Views"
           description="Menu for displaying alternate representations of an object"
          />
          <browser:menu
           id="zmi_actions"
           title="Actions"
           description="Menu for displaying actions to be performed"
          />

          <include package="zope.app.folder" />
        </configure>
        """)

    def test_browser_configuration(self):
        from zope.configuration import xmlconfig

        xmlconfig.string("""
        <configure xmlns="http://namespaces.zope.org/zope"
          xmlns:browser="http://namespaces.zope.org/browser"
          i18n_domain="zope">
          <include package="zope.browsermenu" file="meta.zcml"/>
          <include package="zope.browserpage" file="meta.zcml"/>
          <!-- These normally come from zope.app.zcmlfiles/menus.zcml -->
          <browser:menu
           id="zmi_views"
           title="Views"
           description="Menu for displaying alternate representations of an object"
          />
          <browser:menu
           id="zmi_actions"
           title="Actions"
           description="Menu for displaying actions to be performed"
          />

          <include package="zope.app.folder.browser" />
        </configure>
        """)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
