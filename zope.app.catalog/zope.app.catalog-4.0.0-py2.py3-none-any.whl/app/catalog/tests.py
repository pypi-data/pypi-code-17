##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for backward-compatibility imports

"""

import importlib
import unittest

def _make_import_test(mod_name, attrname):
    def test(self):
        mod = importlib.import_module('zope.app.catalog.' + mod_name)
        self.assertIsNotNone(getattr(mod, attrname, None),
                             str(mod) + ' has no ' + attrname)

    return test

class TestBWCImports(unittest.TestCase):

    for mod_name, attrname in (('attribute', 'AttributeIndex'),
                               ('catalog', 'ResultSet'),
                               ('field', 'FieldIndex'),
                               ('interfaces', 'ICatalog'),
                               ('keyword', 'KeywordIndex'),
                               ('text', 'TextIndex')):
        locals()['test_' + mod_name] = _make_import_test(mod_name, attrname)


from zope.container.contained import Contained
from persistent import Persistent
from zope.pagetemplate.pagetemplate import PageTemplate
from zope.interface import implementer
from zope.index.text.interfaces import ISearchableText

from zope.schema import SourceText


class IZPTPage(ISearchableText):
    """ZPT Pages are a persistent implementation of Page Templates."""

    def setSource(text, content_type='text/html'):
        """Save the source of the page template.

        'text' must be Unicode.
        """

    def getSource():
        """Get the source of the page template."""

    source = SourceText(
        title=u"Source",
        description=u"The source of the page template.",
        required=True)


@implementer(IZPTPage)
class ZPTPage(PageTemplate, Persistent, Contained):

    def getSource(self, request=None):
        return self.read(request)

    def setSource(self, text, content_type='text/html'):
        self.pt_edit(text, content_type)

    # See zope.app.zptpage.interfaces.IZPTPage
    source = property(getSource, setSource, None,
                      """Source of the Page Template.""")

    def getSearchableText(self):
        return self.source


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
