import logging
import os
import tempfile
import unittest

from allinux import shbuiltins


class TestShell(unittest.TestCase):
    """
    All tests are executed in the system temporary directory.
    """

    def setUp(self):
        os.chdir(tempfile.gettempdir())
    
    def test_shell_cd(self):
        shbuiltins.cd()
        self.assertEqual(os.getcwd(), os.environ['HOME'])

    def test_shell_pwd(self):
        self.assertEqual(shbuiltins.pwd(), '/tmp')
