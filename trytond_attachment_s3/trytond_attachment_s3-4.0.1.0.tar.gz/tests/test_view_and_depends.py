#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test_view_depends

    Test Views and Depends

"""
import sys
import os
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase

DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))


class TestViewDependsCase(ModuleTestCase):
    '''
    Test the view and depends
    '''
    module = 'attachment_s3'


def suite():
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestViewDependsCase)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
