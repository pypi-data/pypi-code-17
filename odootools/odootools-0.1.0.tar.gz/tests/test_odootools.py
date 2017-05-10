#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_odootools
----------------------------------

Tests for `odootools` module.
"""


import sys
import unittest

from odootools import odootools


class TestOdootools(unittest.TestCase):

    def setUp(self):
        self.dt_start = '2017-02-27 15:40:55'
        self.dt_stop = '2017-03-01 10:20:20'
        self.start = '2017-02-27'
        self.stop = '2017-03-02'

    def test_dt_range(self):
        dr = odootools.DateRange(self.start, self.stop)
        dates = [x for x in dr]
        results = [
            '2017-02-27',
            '2017-02-28',
            '2017-03-01',
            '2017-03-02',
        ]
        self.assertEqual(dates, results, "DateRange return error, waiting %s and getting %s" % (
            results, dates
        ))

    def test_date_next_day(self):
        date = odootools.Date(self.start).next_day().value
        result = '2017-02-28'
        self.assertEqual(date, result, "Date next day return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_prev_day(self):
        date = odootools.Date(self.start).prev_day().value
        result = '2017-02-26'
        self.assertEqual(date, result, "Date previous day return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_next_month(self):
        date = odootools.Date(self.start).next_month().value
        result = '2017-03-27'
        self.assertEqual(date, result, "Date next month return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_prev_month(self):
        date = odootools.Date(self.start).prev_month().value
        result = '2017-01-27'
        self.assertEqual(date, result, "Date previous month return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_next_year(self):
        date = odootools.Date(self.start).next_year().value
        result = '2018-02-27'
        self.assertEqual(date, result, "Date next year return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_prev_year(self):
        date = odootools.Date(self.start).prev_year().value
        result = '2016-02-27'
        self.assertEqual(date, result, "Date previous year return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_last_day_in_month(self):
        date = odootools.Date(self.start).last_day_in_month().value
        result = '2017-02-28'
        self.assertEqual(date, result, "Date last day in month return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_first_day_in_month(self):
        date = odootools.Date(self.start).first_day_in_month().value
        result = '2017-02-01'
        self.assertEqual(date, result, "Date last day in month return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_date_next_day_month_year(self):
        date = odootools.Date(self.start).next_day().next_month().next_year().value
        result = '2018-03-28'
        self.assertEqual(date, result, "Date next day month and year return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_next_second(self):
        date = odootools.DateTime(self.dt_start).next_second().value
        result = '2017-02-27 15:40:56'
        self.assertEqual(date, result, "DateTime next second return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_prev_second(self):
        date = odootools.DateTime(self.dt_start).prev_second().value
        result = '2017-02-27 15:40:54'
        self.assertEqual(date, result, "DateTime previous second return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_next_minute(self):
        date = odootools.DateTime(self.dt_start).next_minute().value
        result = '2017-02-27 15:41:55'
        self.assertEqual(date, result, "DateTime next minute return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_prev_minute(self):
        date = odootools.DateTime(self.dt_start).prev_minute().value
        result = '2017-02-27 15:39:55'
        self.assertEqual(date, result, "DateTime previous minute return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_next_hour(self):
        date = odootools.DateTime(self.dt_start).next_hour().value
        result = '2017-02-27 16:40:55'
        self.assertEqual(date, result, "DateTime next hour return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_prev_hour(self):
        date = odootools.DateTime(self.dt_start).prev_hour().value
        result = '2017-02-27 14:40:55'
        self.assertEqual(date, result, "DateTime previous hour return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_last_second_in_day(self):
        date = odootools.DateTime(self.dt_start).last_second_in_day().value
        result = '2017-02-27 23:59:59'
        self.assertEqual(date, result, "DateTime last second in the day return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_first_second_in_day(self):
        date = odootools.DateTime(self.dt_start).first_second_in_day().value
        result = '2017-02-27 00:00:00'
        self.assertEqual(date, result, "DateTime first second in the day hour return error, waiting %s and getting %s" % (
            result, date
        ))

    def test_datetime_next_second_minute_hour_day_month_year(self):
        date = odootools.DateTime(self.dt_start).next_second().next_minute().next_hour().next_day().next_month().next_year().value
        result = '2018-03-28 16:41:56'
        self.assertEqual(date, result, "DateTime next second, minute, hour, day, month and year return error, waiting %s and getting %s" % (
            result, date
        ))
