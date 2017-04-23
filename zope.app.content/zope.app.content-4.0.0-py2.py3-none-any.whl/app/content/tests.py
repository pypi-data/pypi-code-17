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
"""Doc test harness for queryType function."""

import doctest
import unittest

from zope import component
from zope.schema.interfaces import IVocabularyFactory
from zope.testing.cleanup import CleanUp
import zope.app.content

class TestConfiguration(CleanUp, unittest.TestCase):

    def test_configuration(self):
        from zope.configuration import xmlconfig
        xmlconfig.file('configure.zcml', package=zope.app.content)

        component.getUtility(IVocabularyFactory, name="Content Types")

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite("zope.app.content"),
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        ))
