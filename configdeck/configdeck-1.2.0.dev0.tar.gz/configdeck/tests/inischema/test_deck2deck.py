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

import sys
import textwrap
import unittest
from io import StringIO

from configdeck.inischema.deck import (
    configdeck,
    ini2schema,
)
from configdeck.deck import schemaconfigdeck


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
        s = "[foo]\nbar = 42\n"
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_main(self):
        s = "[__main__]\nbar = 42\n"
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_none(self):
        s = "[__main__]\nbar = meeeeh\nbar.parser = none"
        _, cg, _ = configdeck(StringIO(s),
                              extra_parsers=[('none', str)])
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_unicode(self):
        s = textwrap.dedent("""
            [__main__]
            bar = zátrapa
        """)
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_int(self):
        s = "[__main__]\nbar = 42\nbar.parser = int\n"
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_bool(self):
        s = "[__main__]\nbar = true\nbar.parser = bool \n"
        _, cg, _ = configdeck(StringIO(s))
        _, sg, _ = schemaconfigdeck(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

if __name__ == '__main__':
    unittest.main()
