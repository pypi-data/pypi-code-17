from __future__ import absolute_import, division, print_function, unicode_literals

from doctest import DocTestSuite

import django
import django.test

from django_otp import oath
from django_otp import util

if django.VERSION < (1, 7):
    from django.utils import unittest
else:
    import unittest


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    suite.addTests(tests)
    suite.addTest(DocTestSuite(util))
    suite.addTest(DocTestSuite(oath))

    return suite


class TestCase(django.test.TestCase):
    """
    Utilities for dealing with custom user models.
    """
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()

        try:
            from django.contrib.auth import get_user_model
        except ImportError:
            from django.contrib.auth.models import User
            cls.User = User
            cls.User.get_username = lambda self: self.username
            cls.USERNAME_FIELD = 'username'
        else:
            cls.User = get_user_model()
            cls.USERNAME_FIELD = cls.User.USERNAME_FIELD

    def create_user(self, username, password):
        """
        Try to create a user, honoring the custom user model, if any.

        This may raise an exception if the user model is too exotic for our
        purposes.

        """
        return self.User.objects.create_user(username, password=password)
