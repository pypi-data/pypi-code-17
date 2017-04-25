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

from io import StringIO
import sys
import textwrap
import unittest

from configdeck.deck import schemaconfigdeck
from configdeck.inischema.deck import (
    configdeck,
    ini2schema,
    )


class TestDeckConvertor(unittest.TestCase):
    def setUp(self):
        # make sure we have a clean sys.argv so as not to have unexpected test
        # results
        self.old_argv = sys.argv
        sys.argv = []

    def tearDown(self):
        # restore old sys.argv
        sys.argv = self.old_argv

    def test_empty(self):
        s = ""
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_simple(self):
        s = textwrap.dedent("""\
            [foo]
            bar = 42
            """)
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_main(self):
        s = textwrap.dedent("""\
            [__main__]
            bar = 42
            """)
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_none(self):
        s = textwrap.dedent("""\
            [__main__]
            bar = meeeeh
            bar.parser = none
            """)
        _, cg, _ = configdeck(
            StringIO(s), extra_parsers=[('none', str)])
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_unicode(self):
        s = textwrap.dedent("""\
            [__main__]
            bar = zátrapa
            """)
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_int(self):
        s = textwrap.dedent("""\
            [__main__]
            bar = 42
            bar.parser = int
            """)
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_bool(self):
        s = textwrap.dedent("""\
            [__main__]
            bar = true
            bar.parser = bool
            """)
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))


if __name__ == '__main__':
    unittest.main()
