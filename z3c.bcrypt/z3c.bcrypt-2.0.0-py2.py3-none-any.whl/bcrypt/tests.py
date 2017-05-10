##############################################################################
#
# Copyright (c) 2007-2008 Zope Foundation and Contributors.
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
import doctest
import re

from zope.testing.renormalizing import OutputChecker
from zope.testing import cleanup

def test_suite():
    checker = OutputChecker([
        (re.compile("u('.*')"), r'\1'),
    ])

    def setUp(_test):
        cleanup.setUp()
    tearDown = setUp

    return doctest.DocFileSuite(
        'USAGE.rst',
        optionflags=doctest.ELLIPSIS,
        checker=checker,
        setUp=setUp,
        tearDown=tearDown,
    )
