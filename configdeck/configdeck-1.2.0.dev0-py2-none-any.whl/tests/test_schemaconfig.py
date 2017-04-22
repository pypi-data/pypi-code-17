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

import unittest
import os
import sys
from io import BytesIO, StringIO
from optparse import (
    OptionConflictError,
    OptionParser,
)

from mock import (
    Mock,
    patch,
)

from configdeck._compat import PY2
from configdeck._compat import NoSectionError
from configdeck.deck import (
    configdeck,
    schemaconfigdeck,
)
from configdeck.parser import SchemaConfigParser
from configdeck.schema import (
    DictOption,
    IntOption,
    Option,
    Schema,
    Section,
    StringOption,
)


# backwards compatibility
if not hasattr(patch, 'object'):
    # mock < 0.8
    from mock import patch_object
    patch.object = patch_object


class TestOption(unittest.TestCase):
    cls = Option

    def test_repr_name(self):
        """Test Option repr with name."""
        opt = self.cls()
        expected = "<{0}>".format(self.cls.__name__)
        self.assertEqual(repr(opt), expected)

        opt = self.cls(name='name')
        expected = "<{0} name>".format(self.cls.__name__)
        self.assertEqual(repr(opt), expected)

        sect = Section(name='sect')
        opt = self.cls(name='name', section=sect)
        expected = "<{0} sect.name>".format(self.cls.__name__)
        self.assertEqual(repr(opt), expected)

    def test_repr_extra(self):
        """Test Option repr with other attributes."""
        opt = self.cls(name='name', raw=True)
        expected = "<{0} name raw>".format(self.cls.__name__)
        self.assertEqual(repr(opt), expected)

        opt = self.cls(name='name', fatal=True)
        expected = "<{0} name fatal>".format(self.cls.__name__)
        self.assertEqual(repr(opt), expected)

        opt = self.cls(name='name', raw=True, fatal=True)
        expected = "<{0} name raw fatal>".format(self.cls.__name__)
        self.assertEqual(repr(opt), expected)

    def test_parse(self):
        """Test Option parse."""
        opt = self.cls()
        self.assertRaises(NotImplementedError, opt.parse, '')

    def test_equal(self):
        """Test Option equality."""
        opt1 = self.cls()
        opt2 = self.cls(name='name', raw=True)

        self.assertEqual(opt1, self.cls())
        self.assertEqual(opt2, self.cls(name='name', raw=True))
        self.assertNotEqual(opt1, opt2)
        self.assertNotEqual(opt1, None)


class TestSection(unittest.TestCase):
    cls = Section

    def test_repr_name(self):
        """Test Section repr method."""
        sect = self.cls()
        expected = "<{0}>".format(self.cls.__name__)
        self.assertEqual(repr(sect), expected)

        sect = self.cls(name='sect')
        expected = "<{0} sect>".format(self.cls.__name__)
        self.assertEqual(repr(sect), expected)

    def test_equal(self):
        """Test Section equality."""
        sec1 = self.cls()
        sec2 = self.cls(name='sec2')

        self.assertEqual(sec1, self.cls())
        self.assertEqual(sec2, self.cls(name='sec2'))
        self.assertNotEqual(sec1, sec2)

    def test_has_option(self):
        """Test Section has_option method."""
        class MySection(self.cls):
            foo = IntOption()

        sec1 = MySection()
        self.assertTrue(sec1.has_option('foo'))
        self.assertFalse(sec1.has_option('bar'))


class TestSchemaConfigDeck(unittest.TestCase):
    def setUp(self):
        class MySchema(Schema):
            class foo(Section):
                bar = IntOption()

            baz = IntOption(help='The baz option')

        self.parser = SchemaConfigParser(MySchema())

    def test_deck_no_op(self):
        """Test schemaconfigdeck with the default OptionParser value."""
        config = BytesIO(b"[__main__]\nbaz=1")
        self.parser.readfp(config)
        self.assertEqual(self.parser.values(),
            {'foo': {'bar': 0}, '__main__': {'baz': 1}})

        op, options, args = schemaconfigdeck(self.parser, argv=['--baz', '2'])
        self.assertEqual(self.parser.values(),
            {'foo': {'bar': 0}, '__main__': {'baz': 2}})

    def test_deck_no_argv(self):
        """Test schemaconfigdeck with the default argv value."""
        config = BytesIO(b"[__main__]\nbaz=1")
        self.parser.readfp(config)
        self.assertEqual(self.parser.values(),
            {'foo': {'bar': 0}, '__main__': {'baz': 1}})

        _argv, sys.argv = sys.argv, []
        try:
            op, options, args = schemaconfigdeck(self.parser)
            self.assertEqual(self.parser.values(),
                {'foo': {'bar': 0}, '__main__': {'baz': 1}})
        finally:
            sys.argv = _argv

    def test_deck_section_option(self):
        """Test schemaconfigdeck overriding one option."""
        config = BytesIO(b"[foo]\nbar=1")
        self.parser.readfp(config)
        self.assertEqual(self.parser.values(),
            {'foo': {'bar': 1}, '__main__': {'baz': 0}})

        op, options, args = schemaconfigdeck(self.parser,
                                             argv=['--foo_bar', '2'])
        self.assertEqual(self.parser.values(),
                         {'foo': {'bar': 2}, '__main__': {'baz': 0}})

    def test_deck_missing_section(self):
        """Test schemaconfigdeck with missing section."""
        class MySchema(Schema):
            foo = DictOption()

        config = BytesIO(b"[__main__]\nfoo = bar")
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)

        # hitting the parser directly raises an exception
        self.assertRaises(NoSectionError, parser.values)
        self.assertFalse(parser.is_valid())

        # which is nicely handled by the stack code, so as not to crash it
        op, options, args = schemaconfigdeck(parser)

        # there is no value for 'foo' due to the missing section
        self.assertEqual(options, {'foo': None})

    def test_deck_json_dict(self):
        class MySchema(Schema):
            foo = DictOption()

        parser = SchemaConfigParser(MySchema())
        op, options, args = schemaconfigdeck(parser,
            argv=['--foo', '{"bar": "baz"}'])

        self.assertEqual(options, {'foo': '{"bar": "baz"}'})
        self.assertEqual(parser.values(),
            {'__main__': {'foo': {'bar': 'baz'}}})

    @patch('configdeck.deck.os')
    def test_deck_environ(self, mock_os):
        mock_os.environ = {'CONFIGDECK_FOO_BAR': '42', 'CONFIGDECK_BAZ': 3}
        config = BytesIO(b"[foo]\nbar=1")
        self.parser.readfp(config)

        _argv, sys.argv = sys.argv, ['prognam']
        try:
            op, options, args = schemaconfigdeck(self.parser)
            self.assertEqual(self.parser.values(),
                {'foo': {'bar': 42}, '__main__': {'baz': 3}})
        finally:
            sys.argv = _argv

    @patch('configdeck.deck.os')
    def test_deck_environ_bad_name(self, mock_os):
        mock_os.environ = {'FOO_BAR': 2, 'BAZ': 3}
        config = BytesIO(b"[foo]\nbar=1")
        self.parser.readfp(config)

        _argv, sys.argv = sys.argv, ['prognam']
        try:
            op, options, args = schemaconfigdeck(self.parser)
            self.assertEqual(self.parser.values(),
                {'foo': {'bar': 1}, '__main__': {'baz': 0}})
        finally:
            sys.argv = _argv

    def test_deck_environ_precedence(self):
        with patch.object(os, 'environ',
            {'CONFIGDECK_FOO_BAR': '42', 'BAR': '1'}):

            config = BytesIO(b"[foo]\nbar=$BAR")
            self.parser.readfp(config)

            _argv, sys.argv = sys.argv, ['prognam']
            try:
                op, options, args = schemaconfigdeck(self.parser)
                self.assertEqual(self.parser.get('foo', 'bar'), 42)
            finally:
                sys.argv = _argv

    def test_deck_environ_precedence_fatal_option(self):
        class MySchema(Schema):
            foo = IntOption(fatal=True)

        parser = SchemaConfigParser(MySchema())

        with patch.object(os, 'environ', {'CONFIGDECK_FOO': '42'}):
            _argv, sys.argv = sys.argv, ['prognam']
            try:
                op, options, args = schemaconfigdeck(parser)
                self.assertEqual(parser.get('__main__', 'foo'), 42)
            finally:
                sys.argv = _argv

    def test_deck_environ_precedence_null_option(self):
        class MySchema(Schema):
            foo = StringOption(null=True)

        parser = SchemaConfigParser(MySchema())

        with patch.object(os, 'environ', {'CONFIGDECK_FOO': '42'}):
            _argv, sys.argv = sys.argv, ['prognam']
            try:
                op, options, args = schemaconfigdeck(parser)
                self.assertEqual(parser.get('__main__', 'foo'), '42')
            finally:
                sys.argv = _argv

    def test_deck_environ_precedence_null_and_fatal_option(self):
        class MySchema(Schema):
            foo = StringOption(null=True, fatal=True)

        parser = SchemaConfigParser(MySchema())

        with patch.object(os, 'environ', {'CONFIGDECK_FOO': '42'}):
            _argv, sys.argv = sys.argv, ['prognam']
            try:
                op, options, args = schemaconfigdeck(parser)
                self.assertEqual(parser.get('__main__', 'foo'), '42')
            finally:
                sys.argv = _argv

    def test_ambiguous_option(self):
        """Test schemaconfigdeck when an ambiguous option is specified."""
        class MySchema(Schema):
            class foo(Section):
                baz = IntOption()

            class bar(Section):
                baz = IntOption()

        config = BytesIO(b"[foo]\nbaz=1")
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values('foo'), {'baz': 1})
        self.assertEqual(parser.values('bar'), {'baz': 0})

        op, options, args = schemaconfigdeck(
            parser, argv=['--bar_baz', '2'])
        self.assertEqual(parser.values('foo'), {'baz': 1})
        self.assertEqual(parser.values('bar'), {'baz': 2})

    def test_help(self):
        """Test schemaconfigdeck with --help."""
        config = BytesIO(b"[foo]\nbar=1")
        self.parser.readfp(config)
        self.assertEqual(self.parser.values(),
            {'foo': {'bar': 1}, '__main__': {'baz': 0}})

        # replace stdout to capture its value
        new_callable = StringIO
        if PY2:
            new_callable = BytesIO
        with patch('sys.stdout', new_callable=new_callable) as mock_stdout:
            # call the method and assert its value
            self.assertRaises(SystemExit, schemaconfigdeck, self.parser,
                argv=['--help'])

        # assert the value of stdout is correct
        output = mock_stdout.getvalue()
        self.assertTrue(output.startswith('Usage:'))

    def test_help_with_fatal(self):
        """Test schemaconfigdeck with --help and an undefined fatal option."""
        class MySchema(Schema):
            foo = IntOption(fatal=True)

        self.parser = SchemaConfigParser(MySchema())

        # replace stdout to capture its value
        new_callable = StringIO
        if PY2:
            new_callable = BytesIO
        with patch('sys.stdout', new_callable=new_callable) as mock_stdout:
            # call the method and assert its value
            self.assertRaises(SystemExit, schemaconfigdeck, self.parser,
                argv=['--help'])

        # assert the value of stdout is correct
        output = mock_stdout.getvalue()
        self.assertTrue(output.startswith('Usage:'))

    def test_parser_set_with_encoding(self):
        """Test schemaconfigdeck override an option with a non-ascii value."""
        class MySchema(Schema):
            foo = StringOption()

        parser = SchemaConfigParser(MySchema())
        op, options, args = schemaconfigdeck(
            parser, argv=['--foo', 'fóobâr'])
        self.assertEqual(parser.get('__main__', 'foo', parse=False),
            'fóobâr')
        self.assertEqual(parser.get('__main__', 'foo'), 'fóobâr')

    def test_option_short_name(self):
        """Test schemaconfigdeck support for short option names."""
        class MySchema(Schema):
            foo = IntOption(short_name='f')

        parser = SchemaConfigParser(MySchema())
        op, options, args = schemaconfigdeck(
            parser, argv=['-f', '42'])
        self.assertEqual(parser.get('__main__', 'foo'), 42)

    def test_option_conflicting_short_name(self):
        """Test schemaconfigdeck with conflicting short option names."""
        class MySchema(Schema):
            foo = IntOption(short_name='f')
            flup = StringOption(short_name='f')

        parser = SchemaConfigParser(MySchema())
        self.assertRaises(OptionConflictError, schemaconfigdeck, parser,
            argv=['-f', '42'])

    def test_option_specified_twice(self):
        """Test schemaconfigdeck with option name specified twice."""
        class MySchema(Schema):
            foo = IntOption(short_name='f')

        parser = SchemaConfigParser(MySchema())
        op, options, args = schemaconfigdeck(
            parser, argv=['-f', '42', '--foo', '24'])
        self.assertEqual(parser.get('__main__', 'foo'), 24)
        op, options, args = schemaconfigdeck(
            parser, argv=['-f', '24', '--foo', '42'])
        self.assertEqual(parser.get('__main__', 'foo'), 42)

    def test_fatal_option_with_config(self):
        class MySchema(Schema):
            foo = IntOption(fatal=True)

        config = BytesIO(b"[__main__]\nfoo=1")
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)

        op, options, args = schemaconfigdeck(parser)
        self.assertEqual(parser.values(), {'__main__': {'foo': 1}})


class ConfigdeckTestCase(unittest.TestCase):
    @patch('configdeck.deck.SchemaConfigParser')
    @patch('configdeck.deck.schemaconfigdeck')
    def test_configdeck_no_errors(self, mock_schemaconfigdeck,
        mock_schema_parser):
        """Test configdeck when no errors occur."""
        # prepare mocks
        expected_schema_parser = Mock()
        expected_schema_parser.is_valid.return_value = (True, None)
        expected_option_parser = Mock()
        expected_options = Mock()
        expected_args = Mock()
        mock_schemaconfigdeck.return_value = (expected_option_parser,
            expected_options, expected_args)
        mock_schema_parser.return_value = expected_schema_parser

        # define the inputs
        class MySchema(Schema):
            foo = IntOption()

        configs = ['config.ini']

        # call the function under test
        deck = configdeck(MySchema, configs)

        # schema_parse is a SchemaConfigParser, initialized with MySchema
        # and fed with the configs file list
        self.assertEqual(deck.schema_parser, expected_schema_parser)
        mock_schema_parser.assert_called_with(MySchema())
        mock_schema_parser.return_value.read.assert_called_with(configs)
        # the other attributes are the result of calling schemaconfigdeck
        mock_schemaconfigdeck.assert_called_with(expected_schema_parser,
            op=None)
        self.assertEqual(deck.option_parser, expected_option_parser)
        self.assertEqual(deck.options, expected_options)
        self.assertEqual(deck.args, expected_args)

    @patch('configdeck.deck.SchemaConfigParser')
    @patch('configdeck.deck.schemaconfigdeck')
    def test_configdeck_with_errors(self, mock_schemaconfigdeck,
        mock_schema_parser):
        """Test configdeck when an error happens."""
        # prepare mocks
        expected_schema_parser = Mock()
        expected_schema_parser.is_valid.return_value = (False, ['some error'])
        expected_option_parser = Mock()
        expected_options = Mock()
        expected_args = Mock()
        mock_schemaconfigdeck.return_value = (expected_option_parser,
            expected_options, expected_args)
        mock_schema_parser.return_value = expected_schema_parser

        # define the inputs
        class MySchema(Schema):
            foo = IntOption()

        configs = ['config.ini']

        # call the function under test
        deck = configdeck(MySchema, configs)

        # schema_parse is a SchemaConfigParser, initialized with MySchema
        # and fed with the configs file list
        self.assertEqual(deck.schema_parser, expected_schema_parser)
        mock_schema_parser.assert_called_with(MySchema())
        mock_schema_parser.return_value.read.assert_called_with(configs)
        # the other attributes are the result of calling schemaconfigdeck
        mock_schemaconfigdeck.assert_called_with(expected_schema_parser,
            op=None)
        self.assertEqual(deck.option_parser, expected_option_parser)
        expected_option_parser.error.assert_called_with('some error')
        self.assertEqual(deck.options, expected_options)
        self.assertEqual(deck.args, expected_args)

    @patch('configdeck.deck.SchemaConfigParser')
    @patch('configdeck.deck.schemaconfigdeck')
    def test_configdeck_with_options(self, mock_schemaconfigdeck,
        mock_schema_parser):
        """Test configdeck with a custom OptionParser."""
        # define the inputs
        class MySchema(Schema):
            foo = IntOption()

        configs = ['config.ini']

        op = OptionParser(usage='foo')

        # prepare mocks
        expected_schema_parser = Mock()
        expected_schema_parser.is_valid.return_value = (True, None)
        expected_args = Mock()
        mock_schemaconfigdeck.return_value = (op,
            op.values, expected_args)
        mock_schema_parser.return_value = expected_schema_parser

        # call the function under test
        deck = configdeck(MySchema, configs, op=op)

        # schema_parse is a SchemaConfigParser, initialized with MySchema
        # and fed with the configs file list
        self.assertEqual(deck.schema_parser, expected_schema_parser)
        mock_schema_parser.assert_called_with(MySchema())
        mock_schema_parser.return_value.read.assert_called_with(configs)
        # the other attributes are the result of calling schemaconfigdeck
        mock_schemaconfigdeck.assert_called_with(expected_schema_parser,
            op=op)
        self.assertEqual(deck.option_parser, op)
        self.assertEqual(deck.options, op.values)
        self.assertEqual(deck.args, expected_args)

    @patch('configdeck.parser.SchemaConfigParser.is_valid')
    def test_configdeck_no_validate(self, mock_is_valid):
        """Test configdeck with validation disabled."""
        mock_is_valid.return_value = (True, [])

        configdeck(Schema, [], validate=False)

        # validation was not invoked
        self.assertEqual(mock_is_valid.called, False)

    @patch('configdeck.parser.SchemaConfigParser.is_valid')
    def test_configdeck_validate(self, mock_is_valid):
        """Test configdeck with validation enabled."""
        mock_is_valid.return_value = (True, [])

        configdeck(Schema, [], validate=True)

        # validation was invoked
        self.assertEqual(mock_is_valid.called, True)

    @patch('configdeck.parser.SchemaConfigParser.is_valid')
    def test_configdeck_validate_default_value(self, mock_is_valid):
        """Test configdeck validation default."""
        mock_is_valid.return_value = (True, [])

        configdeck(Schema, [])

        # validation was not invoked
        self.assertEqual(mock_is_valid.called, False)

    @patch('configdeck.parser.SchemaConfigParser.is_valid')
    def test_configdeck_validate_from_options(self, mock_is_valid):
        """Test configdeck with validation from options."""
        mock_is_valid.return_value = (True, [])

        op = OptionParser()
        op.add_option('--validate', dest='validate', action='store_true')
        with patch.object(sys, 'argv', ['foo', '--validate']):
            configdeck(Schema, [], op=op)

        self.assertEqual(mock_is_valid.called, True)

    @patch('configdeck.parser.SchemaConfigParser.is_valid')
    def test_configdeck_validate_without_option(self, mock_is_valid):
        """Test configdeck with validation from options."""
        mock_is_valid.return_value = (True, [])

        op = OptionParser()
        with patch.object(sys, 'argv', ['foo']):
            configdeck(Schema, [], op=op)

        self.assertEqual(mock_is_valid.called, False)
