import logging
import os
import tempfile
import unittest

from . import coreutils


class TestLinux(unittest.TestCase):
    """
    All tests are executed in the system temporary directory.
    """
    
    def setUp(self):
        os.chdir(tempfile.gettempdir())

    def test_linux_mkdir(self):
        logging.warning(os.getcwd())