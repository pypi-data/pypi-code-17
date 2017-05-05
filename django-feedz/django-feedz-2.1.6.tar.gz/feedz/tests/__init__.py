"""Django feeds test suite"""
import unittest
import os


def suite():
    loader = unittest.TestLoader()
    tests = loader.discover(os.path.dirname(__file__), pattern='test*.py', top_level_dir=None)

    s = unittest.TestSuite()
    for test in tests:
        s.addTest(test)

    return s
