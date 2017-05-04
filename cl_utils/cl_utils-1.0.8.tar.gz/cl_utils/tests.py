"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

#from django.test import TestCase
from testhelpers.testcase import TestCase

class UtilsTest(TestCase):
    def test_is_years_ago(self):
        """
        Tests that is_years_ago gives a valid answer
        """
        import datetime
        import utils
        today_dict = {'year':2009, 'month':6, 'day':11}
        today = datetime.date(**today_dict)
        today_dt = datetime.datetime(hour=15, minute=31, second=31,
                                     **today_dict)
        leapday = datetime.date(year=2008, month=2, day=29)
                                     
        epoch = datetime.datetime(year=1970, month=1, day=1,
                                  hour=0, minute=0, second=0)
        self.assertFalse(utils.is_years_ago(epoch, 1))
        self.assertTrue(utils.is_years_ago(epoch, 40, today_dt))

        birth = datetime.date(year=1996, month=6, day=12)
        self.assertTrue(utils.is_years_ago(birth, 18, today))
        self.assertTrue(utils.is_years_ago(birth, 18, leapday))

        birth = datetime.date(year=1984, month=2, day=29)
        self.assertFalse(utils.is_years_ago(birth, 18))
        self.assertFalse(utils.is_years_ago(birth, 18, leapday))

class MiddlewareTest(TestCase):
    def test_domains_middleware(self):
        pass
