# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import sys
import six
import logging

from grymp import util


class TestPrintError(unittest.TestCase):

    _MESSAGE = 'test message'

    def test_stream(self):
        try:
            sys.stderr = six.StringIO()
            util.print_error(self._MESSAGE)
            self.assertEquals(sys.stderr.getvalue(), self._MESSAGE + '\n')
        finally:
            sys.stderr = sys.__stderr__


class TestDecodeCliArg(unittest.TestCase):

    _ARG_VALUE = 'test_arg_value'

    def test_empty(self):
        with self.assertRaises(ValueError):
            util.decode_cli_arg(None)

    @unittest.skipUnless(sys.version_info.major == 2,
                         'Only applies to Python 2')
    def test_valid_2(self):
        self.assertEqual(
            util.decode_cli_arg(
                self._ARG_VALUE.encode(sys.getfilesystemencoding())),
            self._ARG_VALUE)

    @unittest.skipUnless(sys.version_info.major == 3,
                         'Only applies to Python 3')
    def test_valid_3(self):
        self.assertEqual(util.decode_cli_arg(self._ARG_VALUE), self._ARG_VALUE)


class TestLogLevelFromVerbosity(unittest.TestCase):

    def test_warning(self):
        self.assertEqual(util.log_level_from_vebosity(0), logging.WARNING)

    def test_info(self):
        self.assertEqual(util.log_level_from_vebosity(1), logging.INFO)

    def test_debug(self):
        self.assertEqual(util.log_level_from_vebosity(2), logging.DEBUG)
        self.assertEqual(util.log_level_from_vebosity(None), logging.DEBUG)


class TestRchop(unittest.TestCase):

    _PREFIX = 'foo'
    _SUFFIX = 'bar'

    def test_suffix_removed(self):
        self.assertEqual(util.rchop(self._PREFIX + self._SUFFIX, self._SUFFIX),
                         self._PREFIX)

    def test_unaffected(self):
        string = self._PREFIX + self._SUFFIX + '!'
        self.assertEqual(util.rchop(string, self._SUFFIX), string)


# this class makes assumptions, but fairly safe ones
class TestSameFilesystem(unittest.TestCase):

    def test_same_fs_exists(self):
        self.assertTrue(util.same_filesystem('/', '/root'))

    def test_same_fs_absent(self):
        self.assertTrue(util.same_filesystem('/missing', '/root/missing'))

    def test_different_fs_exists(self):
        self.assertFalse(util.same_filesystem('/', '/dev/shm'))

    def test_different_fs_absent(self):
        self.assertFalse(util.same_filesystem('/missing', '/dev/shm/missing'))
