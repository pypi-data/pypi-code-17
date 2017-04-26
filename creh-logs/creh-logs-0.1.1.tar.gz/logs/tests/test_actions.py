# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import traceback

from django.test import TestCase

from ..utils import get_location
from ..actions import register


class ActionsTestCase(TestCase):

    def test_create(self):
        try:
            result = 10 / 0
        except Exception, e:
            log = register.create_by_exception(e, message=traceback.format_exc(), location=get_location(), tag='Test')

        self.assertEquals(log.title, 'ZeroDivisionError')