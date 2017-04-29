# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import sys
import os
import contextlib
import six

from grymp import __main__ as main


@contextlib.contextmanager
def _suppress_stderr():
    save_stderr = sys.stderr
    try:
        sys.stderr = open(os.devnull, 'w')
        yield
    finally:
        sys.stderr.close()
        sys.stderr = save_stderr


class TestParseArgs(unittest.TestCase):

    _BASE = '/base'
    _NAME = 'name'
    BASE_ARGV = ['grymp', _BASE, _NAME]

    def test_version(self):
        with self.assertRaises(SystemExit), _suppress_stderr():
            main._parse_args(['-V'])

    def test_verbosity_implicit(self):
        self.assertEqual(main._parse_args(self.BASE_ARGV).verbosity, 0)

    def test_verbosity_count(self):
        self.assertEqual(main._parse_args(self.BASE_ARGV +
                                          ['-vvvv']).verbosity,
                         4)

    def test_interactive_missing(self):
        self.assertFalse(main._parse_args(self.BASE_ARGV).interactive)

    def test_interactive(self):
        self.assertTrue(
            main._parse_args(self.BASE_ARGV + ['-i']).interactive)

    def test_overwrite_missing(self):
        self.assertFalse(main._parse_args(self.BASE_ARGV).overwrite)

    def test_overwrite(self):
        self.assertTrue(
            main._parse_args(self.BASE_ARGV + ['-o']).overwrite)

    def test_keep_missing(self):
        self.assertFalse(main._parse_args(self.BASE_ARGV).keep)

    def test_keep(self):
        self.assertTrue(
            main._parse_args(self.BASE_ARGV + ['-k']).keep)

    def test_feature_missing(self):
        self.assertIsNone(main._parse_args(self.BASE_ARGV).feature)

    def test_feature(self):
        feature = 'abc'
        self.assertEqual(
            main._parse_args(self.BASE_ARGV + ['-f', feature]).feature,
            feature)

    def test_extras_missing(self):
        self.assertIsNone(main._parse_args(self.BASE_ARGV).extras)

    def test_extras(self):
        extras = 'def'
        self.assertEqual(
            main._parse_args(self.BASE_ARGV + ['-e', extras]).extras,
            extras)

    def test_base(self):
        self.assertEqual(main._parse_args(self.BASE_ARGV).base, self._BASE)

    def test_name(self):
        self.assertEqual(main._parse_args(self.BASE_ARGV).name, self._NAME)

    # TODO would be great to be able to ensure that either -f or -e is passed
    #      at the argparse level, but it doesn't seem to be able to handle it:
    #      http://stackoverflow.com/questions/6722936
    #      tested below for the time being


class TestMain(unittest.TestCase):

    def test_feature_or_model(self):
        with _suppress_stderr():
            self.assertEqual(main.main(TestParseArgs.BASE_ARGV), 1)
