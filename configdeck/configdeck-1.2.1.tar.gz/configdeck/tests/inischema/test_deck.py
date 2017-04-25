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

from io import BytesIO, StringIO, TextIOWrapper
import sys
import textwrap
import unittest

from mock import patch

from configdeck._compat import PY2
from configdeck.inischema.deck import configdeck
from configdeck.parser import CONFIG_FILE_ENCODING


class TestBase(unittest.TestCase):
    """ Base class to keep common set-up """
    def setUp(self):
        self.file = TextIOWrapper(BytesIO(self.ini))
        self.old_sys_argv = sys.argv
        sys.argv = ['']

    def tearDown(self):
        sys.argv = self.old_sys_argv


class TestDeck(TestBase):
    ini = textwrap.dedent('''\
        [blah]
        foo.help = yadda yadda yadda
            yadda
        foo.metavar = FOO
        foo.parser = int
        foo = 2
        ''').encode(CONFIG_FILE_ENCODING)
    arg = '--blah_foo'
    opt = 'blah_foo'
    val = 2

    def test_ini_file_wins_when_no_args(self):
        parser, options, args = configdeck(self.file, args=[])
        self.assertEqual(vars(options), {self.opt: self.val})

    def test_args_win(self):
        parser, options, args = configdeck(
            self.file, args=['', self.arg + '=5'])
        self.assertEqual(vars(options), {self.opt: '5'})

    def test_help_is_displayed(self):
        new_callable = StringIO
        if PY2:
            new_callable = BytesIO

        with patch('sys.stdout', new_callable=new_callable) as mock_stdout:
            try:
                configdeck(self.file, args=['', '--help'])
            except SystemExit:
                output = mock_stdout.getvalue()
        self.assertTrue('yadda yadda yadda yadda' in output)


class TestCrazyDeck(TestDeck):
    ini = textwrap.dedent('''\
        [bl-ah]
        foo.default = 3
        foo.help = yadda yadda yadda
            yadda
        foo.metavar = FOO
        foo.parser = int
        foo = 2
        ''').encode(CONFIG_FILE_ENCODING)
    arg = '--bl-ah_foo'
    opt = 'bl_ah_foo'


class TestNoValue(TestDeck):
    ini = textwrap.dedent('''\
        [blah]
        foo.help = yadda yadda yadda
            yadda
        foo.metavar = FOO
        foo.parser = int
        foo = 3
        ''').encode(CONFIG_FILE_ENCODING)
    val = 3


class TestDeck2(TestBase):
    ini = textwrap.dedent("""\
        [__main__]
        a=1
        """).encode(CONFIG_FILE_ENCODING)

    def test_main(self):
        parser, options, args = configdeck(self.file)
        self.assertEqual(options.a, '1')


class TestDeck3(TestBase):
    ini = textwrap.dedent("""\
        [x]
        a.help=hi
        """).encode(CONFIG_FILE_ENCODING)

    def test_empty(self):
        parser, options, args = configdeck(self.file)
        self.assertEqual(options.x_a, '')

    def test_accepts_args_and_filenames(self):
        parser, options, args = configdeck(
            self.file, 'dummy', args=['', '--x_a=1'])
        self.assertEqual(options.x_a, '1')


class TestDeckShortName(TestBase):
    ini = textwrap.dedent("""\
        [x]
        long_opt.short_name=L
        """).encode(CONFIG_FILE_ENCODING)

    def test_accepts_long_args(self):
        parser, options, args = configdeck(
            self.file, 'dummy', args=['', '--x_long_opt=13579'])
        self.assertEqual(options.x_long_opt, '13579')

    def test_accepts_short_args(self):
        parser, options, args = configdeck(
            self.file, 'dummy', args=['', '-L86420'])
        self.assertEqual(options.x_long_opt, '86420')

    def test_help_displays_both_args(self):
        new_callable = StringIO
        if PY2:
            new_callable = BytesIO

        with patch('sys.stdout', new_callable=new_callable) as mock_stdout:
            try:
                configdeck(self.file, args=['', '--help'])
            except SystemExit:
                output = mock_stdout.getvalue()
        self.assertTrue('-L X_LONG_OPT, --x_long_opt=X_LONG_OPT' in output)


class TestDeckBool(TestBase):
    ini = textwrap.dedent('''\
        [__main__]
        foo.parser=bool
        foo.action=store_true

        bar.default = True
        bar.parser = bool
        bar.action = store_false
        ''').encode(CONFIG_FILE_ENCODING)

    def test_store_true(self):
        parser, options, args = configdeck(self.file, args=['', '--foo'])
        self.assertEqual(options.foo, True)

    def test_store_false(self):
        parser, options, args = configdeck(self.file, args=['', '--bar'])
        self.assertEqual(options.bar, False)


class TestDeckLines(TestBase):
    ini = textwrap.dedent('''\
        [__main__]
        foo.parser = lines
        foo.action = append

        bar = a
            b
        bar.parser = lines
        bar.action = append
        ''').encode(CONFIG_FILE_ENCODING)

    def test_nothing(self):
        parser, options, args = configdeck(self.file)
        self.assertEqual(options.foo, [])

    def test_no_append(self):
        parser, options, args = configdeck(self.file)
        self.assertEqual(options.bar, ['a', 'b'])

    def test_append_on_empty(self):
        parser, options, args = configdeck(self.file, args=['', '--foo=x'])
        self.assertEqual(options.foo, ['x'])

    def test_append(self):
        parser, options, args = configdeck(self.file, args=['', '--bar=x'])
        self.assertEqual(options.bar, ['a', 'b', 'x'])
