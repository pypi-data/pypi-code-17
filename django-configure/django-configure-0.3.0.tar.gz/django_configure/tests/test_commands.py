
import os

import io

from django.core.management.base import CommandError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.testapp.settings')
import tempfile
import unittest

import shutil

import django
from django.core.management import call_command
from django.test import TestCase


class CommandsTestCase(TestCase):
    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def setUp(self):
        super(CommandsTestCase, self).setUp()
        django.setup()
        self.tmp_dir = os.path.join(tempfile.gettempdir(), 'django-config-test')
        self.config_path = os.path.join(self.tmp_dir, 'testapp.cfg')
        self.base_path = os.path.join(os.path.dirname(__file__), 'testapp')

    def test_e2e_config_gen(self):

        args = [self.config_path]
        opts = {}

        call_command('createconfig', *args, dev=False)
        call_command('createconfig', *args, dev=True)

    def test_e2e_config_gen_no_django_def(self):
        """
        Tests whether correct error is shown if user tries to generate config without first specyfing it in
        django settings.py
        """
        import django_configure
        django_configure.main_config = None
        out = io.StringIO()
        self.assertRaises(CommandError, call_command, 'createconfig', [self.config_path], dev=False, stdout=out)
        print((out.getvalue()))


if __name__ == '__main__':
    unittest.main()
