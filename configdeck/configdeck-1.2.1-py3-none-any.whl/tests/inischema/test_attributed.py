# -*- coding: utf-8 -*-
###############################################################################
#
# configdeck -- Stacked configuration sources for your application.
#
# A library for simple, DRY configuration of applications
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
# Copyright © 2009–2013 Canonical Ltd.
#
# This is free software; see the file ‘COPYING’ for details.
#
###############################################################################

from __future__ import unicode_literals

# in testfiles, putting docstrings on methods messes up with the
# runner's output, so pylint: disable-msg=C0111

from io import StringIO
import textwrap
import unittest

from configdeck._compat import RawConfigParser
from configdeck.inischema.attributed import AttributedConfigParser


class BaseTest(unittest.TestCase):
    """ Base class to keep common set-up """
    def setUp(self):
        self.config_string = textwrap.dedent('''\
            [xyzzy]
            foo         = 5
            foo.banana  = yellow
            foo.mango   = orange
            foo.noise   = white

            bar.blah    = 23
            ''')
        self.config = AttributedConfigParser()
        self.config.read_file(StringIO(self.config_string))


class TestAttributed(BaseTest):
    """ pretty basic tests of AttributedConfigParser """
    def test_config_before_parsing_is_plain(self):
        raw_config = RawConfigParser()
        raw_config.read_file(StringIO(self.config_string))
        self.assertEqual(
            [
                (section, sorted(self.config.items(section)))
                for section in self.config.sections()],
            [
                (section, sorted(raw_config.items(section)))
                for section in raw_config.sections()])

    def test_config_after_parsing_is_attributed(self):
        self.config.parse_all()
        self.assertEqual(
            self.config.get('xyzzy', 'foo').attrs['noise'],
            'white')

    def test_config_after_parsing_still_knows_about_empty_values(self):
        self.config.parse_all()
        self.assertTrue(self.config.get('xyzzy', 'bar').is_empty)
