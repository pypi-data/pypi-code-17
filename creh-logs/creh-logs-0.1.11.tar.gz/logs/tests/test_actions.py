# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import traceback

from django.db.models.loading import get_model
from django.test import TestCase
from django.conf import settings

from ..utils import get_location
from ..actions import register
from .. import contstants


class ActionsTestCase(TestCase):

    def create_user(self):
        user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
        User = get_model(user_model.split('.')[0], user_model.split('.')[1])
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        return user

    def test_register_exception(self):
        try:
            result = 10 / 0
        except Exception, e:
            log = register.create_by_exception(e, message=traceback.format_exc(), location=get_location(), tag='Test')

        self.assertEquals(log.title, 'ZeroDivisionError')
        self.assertEquals(log.status, contstants.STATUS_ACTIVE)
        self.assertEquals(log.level, contstants.LEVEL_ERROR)

    def test_register_exception_log(self):
        try:
            result = 10 / 0
        except Exception, e:
            log = register.create_log('Esta es una advertencia', level=contstants.LEVEL_WARNING,
                                      message=traceback.format_exc(), location=get_location(), tag='Test')
        self.assertEquals(log.title, 'Esta es una advertencia')
        self.assertEquals(log.status, contstants.STATUS_ACTIVE)
        self.assertEquals(log.level, contstants.LEVEL_WARNING)

    def test_register_info_log(self):
        user = self.create_user()
        register.create_log(title='Charge succeeded', user=user, message='', tag='CHARGE')