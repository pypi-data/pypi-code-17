# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase
from django.db.models.loading import get_model

from ..utils import get_location, verify_user, verify_exception


class UtilsTestCase(TestCase):

    def create_user(self):
        user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
        User = get_model(user_model.split('.')[0], user_model.split('.')[1])
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        return user

    def test_get_location(self):
        location = ''
        try:
            result = 10 / 0
        except Exception, e:
            location = get_location()
        self.assertTrue('test_utils.py 22' in location)

    def test_verify_user(self):
        user = self.create_user()
        user_verified = verify_user(user)
        self.assertEquals(user, user_verified)

    def test_verify_exception(self):
        exception_verified = None
        exception_name = ''
        try:
            result = 10 / 0
        except Exception, e:
            exception_name = e.__class__.__name__
            exception_verified = verify_exception(e)

        self.assertEquals(exception_verified, exception_name)