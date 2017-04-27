# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import traceback

from django.test import TestCase

from ..utils import get_location
from ..actions import register
from .. import contstants


class ActionsTestCase(TestCase):

    def test_register_exception(self):
        try:
            result = 10 / 0
        except Exception, e:
            log = register.create_by_exception(e, message=traceback.format_exc(), location=get_location(), tag='Test')

        self.assertEquals(log.title, 'ZeroDivisionError')
        self.assertEquals(log.status, contstants.STATUS_ACTIVE)
        self.assertEquals(log.level, contstants.LEVEL_ERROR)

    def test_register_log(self):
        try:
            result = 10 / 0
        except Exception, e:
            log = register.create_log('Esta es una advertencia', message=traceback.format_exc(), location=get_location(), tag='Test')
        self.assertEquals(log.title, 'Esta es una advertencia')
        self.assertEquals(log.status, contstants.STATUS_ACTIVE)
        self.assertEquals(log.level, contstants.LEVEL_WARNING)