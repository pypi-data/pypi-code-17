# tests/test_metadata.py
# Part of Mail Drake, an email server for development and testing.
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit test for `_metadata` private module. """

import collections
import errno
import functools
import io
import json
import re
import unittest.mock
import urllib.parse

import pkg_resources
import testscenarios
import testtools
import testtools.helpers
import testtools.matchers

from .. import _metadata


class DistributionVersionUnknown_TestCase(unittest.TestCase):
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
        unittest.TestCase):
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
        self.mock_open = unittest.mock.mock_open()
        self.open_patcher = unittest.mock.patch.object(
                _metadata, 'open', new=self.mock_open)

        if hasattr(self, 'open_exception'):
            self.mock_open.side_effect = self.open_exception
        else:
            self.mock_open.return_value = self.datafile
        if hasattr(self, 'file_exception'):
            self.datafile.read = unittest.mock.MagicMock(
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


class get_version_fields_TestCase(
        testscenarios.WithScenarios,
        unittest.TestCase):
    """ Test cases for function `get_version_fields`. """

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.test_datafile_path = "/lorem/ipsum"
        self.test_version_text = "17.42.64"
        self.patch_get_version_text(self.test_version_text)

    def patch_get_version_text(self, version_text):
        """ Patch the `get_version_text` function for this test case. """
        func_patcher = unittest.mock.patch.object(
                _metadata, 'get_version_text',
                return_value=version_text)
        self.mock_get_version_text = func_patcher.start()
        self.addCleanup(func_patcher.stop)

    @unittest.mock.patch.object(_metadata, 'semver')
    def test_calls_get_version_text_with_specified_path(
            self,
            mock_semver,
    ):
        """ Should call `get_version_text` with specified path. """
        _metadata.get_version_fields(self.test_datafile_path)
        self.mock_get_version_text.assert_called_with(self.test_datafile_path)

    @unittest.mock.patch.object(_metadata, 'semver')
    def test_calls_get_version_text_with_default_path(
            self,
            mock_semver,
    ):
        """ Should call `get_version_text` with default path. """
        _metadata.get_version_fields()
        expected_path = _metadata.version_file_path
        self.mock_get_version_text.assert_called_with(expected_path)

    @unittest.mock.patch.object(_metadata, 'semver')
    def test_calls_semver_parse_with_version_text(
            self,
            mock_semver,
    ):
        """ Should call `semver.parse` with version text from file. """
        _metadata.get_version_fields(self.test_datafile_path)
        mock_semver.parse.assert_called_with(self.test_version_text)

    @unittest.mock.patch.object(_metadata, 'semver', new=NotImplemented)
    def test_raises_exception_when_semver_notimplemented(self):
        """ Should raise `DistributionVersionUnknown` when no `semver`.

            The version fields are parsed using the `semver` library;
            without that library, the fields are unknown.
            """
        expected_exception = _metadata.DistributionVersionUnknown
        with self.assertRaises(expected_exception) as context:
            _metadata.get_version_fields(self.test_datafile_path)
        self.assertIn('semver', str(context.exception))

    @unittest.mock.patch.object(_metadata, 'semver')
    def test_raises_exception_when_semver_parse_error(
            self,
            mock_semver,
    ):
        """ Should raise `DistributionVersionUnknown` when parse error.

            When the `semver.parse` function raises a `ValueError`,
            the version string can't be parsed; the version fields are
            unknown.
            """
        mock_semver.parse.side_effect = ValueError("failed to parse")
        expected_exception = _metadata.DistributionVersionUnknown
        with self.assertRaises(expected_exception) as context:
            _metadata.get_version_fields(self.test_datafile_path)
        self.assertIn(self.test_datafile_path, str(context.exception))

    @unittest.mock.patch.object(_metadata, 'semver')
    def test_returns_expected_result_for_version(
            self,
            mock_semver,
    ):
        """ Should return expected result for parsed version. """
        fake_parse_result = {
            'major': object(),
            'minor': object(),
            'patch': object(),
            'prerelease': object(),
            'build': object(),
            }
        mock_semver.parse.return_value = fake_parse_result
        result = _metadata.get_version_fields(self.test_datafile_path)
        expected_fields = fake_parse_result
        expected_fields.update(text=self.test_version_text)
        self.assertEqual(result, expected_fields)


class HasAttribute(testtools.matchers.Matcher):
    """ A matcher to assert an object has a named attribute. """

    def __init__(self, name):
        self.attribute_name = name

    def match(self, instance):
        """ Assert the object `instance` has an attribute named `name`. """
        result = None
        if not testtools.helpers.safe_hasattr(instance, self.attribute_name):
            result = AttributeNotFoundMismatch(instance, self.attribute_name)
        return result


class AttributeNotFoundMismatch(testtools.matchers.Mismatch):
    """ The specified instance does not have the named attribute. """

    def __init__(self, instance, name):
        self.instance = instance
        self.attribute_name = name

    def describe(self):
        """ Emit a text description of this mismatch. """
        text = (
                "{instance!r}"
                " has no attribute named {name!r}").format(
                    instance=self.instance, name=self.attribute_name)
        return text


class metadata_value_TestCase(
        testscenarios.WithScenarios,
        testtools.TestCase):
    """ Test cases for metadata module values. """

    expected_str_attributes = set([
            'version_info',
            'version_text',
            'author',
            'copyright',
            'license',
            'url',
            ])

    scenarios = [
            (name, {'attribute_name': name})
            for name in expected_str_attributes]
    for (name, params) in scenarios:
        if name == 'version_info':
            params['expected_type'] = tuple
            continue
        params['expected_type'] = str

    def test_module_has_attribute(self):
        """ Metadata should have expected value as a module attribute. """
        self.assertThat(
                _metadata, HasAttribute(self.attribute_name))

    def test_module_attribute_has_type(self):
        """ Metadata value should be an instance of expected type. """
        instance = getattr(_metadata, self.attribute_name)
        self.assertIsInstance(instance, self.expected_type)


class YearRange_TestCase(
        testscenarios.WithScenarios,
        unittest.TestCase):
    """ Test cases for ‘YearRange’ class. """

    scenarios = [
            ('simple', {
                'begin_year': 1970,
                'end_year': 1979,
                'expected_text': "1970–1979",
                }),
            ('same year', {
                'begin_year': 1970,
                'end_year': 1970,
                'expected_text': "1970",
                }),
            ('no end year', {
                'begin_year': 1970,
                'end_year': None,
                'expected_text': "1970",
                }),
            ]

    def setUp(self):
        """ Set up test fixtures. """
        super().setUp()

        self.test_instance = _metadata.YearRange(
                self.begin_year, self.end_year)

    def test_text_representation_as_expected(self):
        """ Text representation should be as expected. """
        result = str(self.test_instance)
        self.assertEqual(result, self.expected_text)


FakeYearRange = collections.namedtuple('FakeYearRange', ['begin', 'end'])


@unittest.mock.patch.object(_metadata, 'YearRange', new=FakeYearRange)
class make_year_range_TestCase(
        testscenarios.WithScenarios,
        unittest.TestCase):
    """ Test cases for ‘make_year_range’ function. """

    scenarios = [
            ('simple', {
                'begin_year': "1970",
                'end_date': "1979-01-01",
                'expected_range': FakeYearRange(begin=1970, end=1979),
                }),
            ('same year', {
                'begin_year': "1970",
                'end_date': "1970-01-01",
                'expected_range': FakeYearRange(begin=1970, end=1970),
                }),
            ('no end year', {
                'begin_year': "1970",
                'end_date': None,
                'expected_range': FakeYearRange(begin=1970, end=None),
                }),
            ('end date UNKNOWN token', {
                'begin_year': "1970",
                'end_date': "UNKNOWN",
                'expected_range': FakeYearRange(begin=1970, end=None),
                }),
            ('end date FUTURE token', {
                'begin_year': "1970",
                'end_date': "FUTURE",
                'expected_range': FakeYearRange(begin=1970, end=None),
                }),
            ]

    def test_result_matches_expected_range(self):
        """ Result should match expected YearRange. """
        result = _metadata.make_year_range(self.begin_year, self.end_date)
        self.assertEqual(result, self.expected_range)


class metadata_content_TestCase(testtools.TestCase):
    """ Test cases for content of metadata. """

    def test_copyright_formatted_correctly(self):
        """ Copyright statement should be formatted correctly. """
        regex_pattern = (
                "Copyright © "
                "\d{4}"  # Four-digit year.
                "(?:–\d{4})?"  # Optional range dash and four-digit year.
                )
        regex_flags = re.UNICODE
        self.assertThat(
                _metadata.copyright,
                testtools.matchers.MatchesRegex(regex_pattern, regex_flags))

    def test_author_formatted_correctly(self):
        """ Author information should be formatted correctly. """
        regex_pattern = (
                ".+ "  # Name.
                "<[^>]+>"  # Email address, in angle brackets.
                )
        regex_flags = re.UNICODE
        self.assertThat(
                _metadata.author,
                testtools.matchers.MatchesRegex(regex_pattern, regex_flags))

    def test_copyright_contains_author(self):
        """ Copyright information should contain author information. """
        self.assertThat(
                _metadata.copyright,
                testtools.matchers.Contains(_metadata.author))

    def test_url_parses_correctly(self):
        """ Homepage URL should parse correctly. """
        result = urllib.parse.urlparse(_metadata.url)
        self.assertIsInstance(
                result, urllib.parse.ParseResult,
                "URL value {url!r} did not parse correctly".format(
                    url=_metadata.url))


# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.AGPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
