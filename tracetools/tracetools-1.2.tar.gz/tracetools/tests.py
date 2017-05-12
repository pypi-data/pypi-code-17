#!/usr/bin/env python

import unittest
from tracetools import dump


class TestIsoTools(unittest.TestCase):
    """
    dump()
    """
    def test_dump_short_message(self):
        self.assertEqual(dump(b'iddqd'), '\t69 64 64 71 64                                          iddqd\n\t')

    def test_dump_one_line_ascii(self):
        self.assertEqual(dump(b'testdatatestdata'), '\t74 65 73 74 64 61 74 61 74 65 73 74 64 61 74 61         testdatatestdata\n\t')

    def test_dump_one_line_non_ascii(self):
        self.assertEqual(dump(b'\x11\x12\x13\x14datatestdata'), '\t11 12 13 14 64 61 74 61 74 65 73 74 64 61 74 61         ....datatestdata\n\t')

    def test_dump_two_lines_ascii(self):
        self.assertEqual(dump(b'loremipsumdolorsitamet'), '\t6c 6f 72 65 6d 69 70 73 75 6d 64 6f 6c 6f 72 73         loremipsumdolors\n\t69 74 61 6d 65 74                                       itamet\n\t')

if __name__ == '__main__':
    unittest.main()