#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sqloose
----------------------------------

Tests for `sqloose` module.
"""

import os
import sys
import unittest

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../")))

from sqloose import sqloose, cli

class TestSqloose(unittest.TestCase):

    def test_straight_sql(self):
        basic = u"select a,b,c from database where a=1 group by 1 order by 1"
        sql = sqloose.to_sql(basic)
        self.assertEqual(basic, sql)

    def test_straight_sql_string(self):
        basic = u"select a,b,c from database where a=1 group by a order by 1"
        sql = sqloose.to_sql(basic)
        self.assertEqual(basic, sql)

    def test_order_by_negative_index(self):
        onset = u"select a,b,c from database where a=1 group by 1 order by -1"

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, u"select a,b,c from database where a=1 group by 1 order by 3")

    def test_group_by_negative_index(self):
        onset = u"select a,b,c from database where a=1 group by -1 order by 1"

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, u"select a,b,c from database where a=1 group by 3 order by 1")

    def test_subgroup(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                 "group by 1 order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1 order by 3"))

    def test_single_item_range(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                 "group by [1] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1 order by 3"))

    def test_single_item_range_string(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                 "group by [a] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by a order by 3"))

    def test_single_item_range_negative(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                 "group by [-1] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 3 order by 3"))

    def test_range_start_numeric(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [1:] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2,3 order by 3"))

    def test_range_end_numeric(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [:2] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2 order by 3"))

    def test_two_sided_range_numeric(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [1:2] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2 order by 3"))

    def test_range_equal_numeric(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [2:2] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 2 order by 3"))

    def test_range_start_string(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [a:2] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2 order by 3"))

    def test_range_end_string(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [:b] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2 order by 3"))

    def test_two_sided_range_string(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [a:c] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2,3 order by 3"))

    def test_range_equal_string(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [b:b] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 2 order by 3"))

    def test_two_sided_range_mixed(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [1:b] order by -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2 order by 3"))

    def test_preserves_capitalization(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [1] order BY -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1 order BY 3"))

    def test_negative_out_of_range(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [1] order BY -4")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_range_reversed(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [2:-3] order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_order_option(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [1] order BY -1 asc, -2 DESC")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1 order BY 3 asc, 2 DESC"))

    def test_group_to(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group to 2 order BY -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1 order BY 3"))

    def test_group_through(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group through 2 order BY -1")

        sql = sqloose.to_sql(onset)
        self.assertEqual(sql, (u"select a,b,c from database where a in "
                               "(select a from new group by 1) group by 1,2 order BY 3"))

    def test_range_left_not_existing(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [e:2] order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_range_right_not_existing(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [2:e] order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_group_to_1(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group to 1 order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_group_to_range(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group to [1:2] order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_group_through_range(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group through [1:2] order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_ummatched_brackets_left(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by [1:2 order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_ummatched_brackets_right(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group by 1:2] order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_invalid_group_type(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group via 2 order BY -1")

        self.assertRaises(ValueError, sqloose.to_sql, onset)

    def test_statement_to_sql_wrong_type(self):
        onset = ("select a,b,c from database where a in (select a from new group by -1) "
                "group via 2 order BY -1")

        self.assertRaises(TypeError, sqloose.statement_to_sql, onset)

if __name__ == '__main__':
    sys.exit(unittest.main())
