# -*- coding: utf-8 -*-
###############################################################################
#
# configdeck -- Stacked configuration sources for your application.
#
# A library for simple, DRY configuration of applications
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software; see the file ‘COPYING’ for details.
#
###############################################################################

""" Unit tests for the ‘_metadata’ implementation module. """

from __future__ import unicode_literals

import errno
import io
import unittest

import mock
import testscenarios
import unittest2

from .. import _metadata


class DistributionVersionUnknown_TestCase(unittest2.TestCase):
    """ Test cases for class `DistributionVersionUnknown`. """

    def test_has_expected_classes(self):
        """ Should inherit from expected classes. """
        instance = _metadata.DistributionVersionUnknown("b0gUs")
        expected_classes = [ValueError]
        for expected_class in expected_classes:
            with self.subTest(expected_class=expected_class):
                self.assertIsInstance(instance, expected_class)


class get_version_text_TestCase(
        testscenarios.WithScenarios,
        unittest2.TestCase):
    """ Test cases for function `get_version_text`. """

    file_path_scenarios = [
            ('named-path', {
                'datafile_path': "lorem.conf",
                'expected_open_path': "lorem.conf",
                }),
            ('default-path', {
                'expected_open_path': _metadata.version_file_path,
                }),
            ]

    file_content_scenarios = [
            ('simple-version', {
                'datafile_content': "0.1.2\n",
                'expected_result': "0.1.2",
                }),
            ]

    file_result_scenarios = [
            ('read-okay', {}),
            ('error-notfound', {
                'open_exception': IOError(
                    errno.ENOENT, "No such file or directory"),
                'expected_error': _metadata.DistributionVersionUnknown,
                }),
            ('error-permissiondenied', {
                'file_exception': OSError(
                    errno.EPERM, "Permission denied"),
                'expected_error': _metadata.DistributionVersionUnknown,
                }),
            ]

    scenarios = testscenarios.multiply_scenarios(
            file_path_scenarios,
            file_content_scenarios,
            file_result_scenarios,
            )

    def setUp(self):
        """ Set up fixtures for this test case. """
        self.test_args = {}
        try:
            self.test_args['datafile_path'] = self.datafile_path
        except AttributeError:
            pass

        self.datafile = io.StringIO(self.datafile_content)
        self.patch_open()

    def patch_open(self):
        """ Patch the `open` function for this test case. """
        self.mock_open = mock.mock_open()
        self.open_patcher = mock.patch.object(
                _metadata, 'open', new=self.mock_open)

        if hasattr(self, 'open_exception'):
            self.mock_open.side_effect = self.open_exception
        else:
            self.mock_open.return_value = self.datafile
        if hasattr(self, 'file_exception'):
            self.datafile.read = mock.MagicMock(
                self.datafile.read, side_effect=self.file_exception)

    def test_opens_datafile_path(self):
        """ Should call `open` with the expected `datafile_path`. """
        with self.open_patcher:
            if hasattr(self, 'expected_error'):
                with self.assertRaises(self.expected_error):
                    _metadata.get_version_text(**self.test_args)
            else:
                _metadata.get_version_text(**self.test_args)
        self.mock_open.assert_called_with(self.expected_open_path)

    def test_gives_expected_result(self):
        """ Should give expected result for file content. """
        with self.open_patcher:
            if hasattr(self, 'expected_error'):
                with self.assertRaises(self.expected_error):
                    _metadata.get_version_text(**self.test_args)
            else:
                result = _metadata.get_version_text(**self.test_args)
                self.assertEqual(result, self.expected_result)


if __name__ == '__main__':
    unittest.main()
