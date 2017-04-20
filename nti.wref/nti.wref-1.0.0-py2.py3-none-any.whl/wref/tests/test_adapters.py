#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

import unittest

from persistent import Persistent

from nti.wref.interfaces import IWeakRef

from nti.wref.tests import SharedConfiguringTestLayer


class TestAdapters(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_persistent(self):

        class Base(Persistent):
            pass

        base = Base()
        ref = IWeakRef(base, None)
        assert_that(ref, is_not(none()))

