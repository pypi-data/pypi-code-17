import unittest
import subprocess
from test.test_support import EnvironmentVarGuard

from mock import Mock

from outlyer.plugin_helper.container import _subprocess


class TestSubprocess(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentVarGuard()

    def test_patch_container(self):
        _subprocess.patch()
        self.assertTrue(hasattr(subprocess, '_check_output'))

    def test_unpatch_container(self):
        _subprocess.unpatch()
        self.assertFalse(hasattr(subprocess, '_check_output'))

    def test_check_output_no_container_patched(self):
        self.env.unset('CONTAINER_ID')
        _subprocess.patch()
        subprocess._check_output = Mock()
        subprocess.check_output = Mock()
        _subprocess.check_output(['ls', '/tmp'])
        subprocess._check_output.assert_called_with(['ls', '/tmp'])
        subprocess.check_output.assert_not_called()

    def test_check_output_no_container_not_patched(self):
        self.env.unset('CONTAINER_ID')
        _subprocess.unpatch()
        subprocess.check_output = Mock()
        _subprocess.check_output(['ls', '/tmp'])
        subprocess.check_output.assert_called_with(['ls', '/tmp'])