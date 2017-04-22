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

"""Tests! Who woulda said"""

# Two use cases so far for this file:
#  * make tests a package, so setup.py's "test" command finds the tests
#  * load all the tests

if __name__ == '__main__':
    import unittest

    from configdeck.tests import (test_attributed, test_typed,
                                  test_parsers, test_deck, test_deck2deck)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for module in (
            test_attributed, test_typed, test_parsers, test_deck,
            test_deck2deck):
        suite.addTest(loader.loadTestsFromModule(module))

    unittest.TextTestRunner(verbosity=2).run(suite)
