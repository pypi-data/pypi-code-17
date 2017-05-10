# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from past.builtins import basestring

class Date:
    """docstring for Date"""

    def __init__(self, date, fmt='%Y-%m-%d'):
        if isinstance(date, datetime):
            date = date.strftime(fmt)
        self._date = date
        self._fmt = fmt

    @property
    def value(self):
        return self._date

    def _apply(self, days=None, day=None, months=None, month=None, years=None, year=None):
        date = datetime.strptime(self._date, self._fmt)
        if days is not None:
            date = date + relativedelta(days=days)
        if day is not None:
            date = date + relativedelta(day=day)
        if months is not None:
            date = date + relativedelta(months=months)
        if month is not None:
            date = date + relativedelta(month=month)
        if years is not None:
            date = date + relativedelta(years=years)
        if year is not None:
            date = date + relativedelta(year=year)
        self._date = date.strftime(self._fmt)
        return self

    def next_day(self, days=1):
        return self._apply(days=days)

    def prev_day(self, days=1):
        return self._apply(days=-1 * days)

    def first_day_in_month(self):
        return self._apply(day=1)

    def last_day_in_month(self):
        date = datetime.strptime(self._date, self._fmt)
        day = calendar.monthrange(date.year, date.month)[1]
        return self._apply(day=day)

    def next_month(self, months=1):
        return self._apply(months=months)

    def prev_month(self, months=1):
        return self._apply(months=-1 * months)

    def next_year(self, years=1):
        return self._apply(years=years)

    def prev_year(self, years=1):
        return self._apply(years=-1 * years)

    def __add__(self, other):
        return self._apply(days=other)

    def __str__(self):
        return self.value


class DateTime(Date):
    """docstring for DateTime"""

    def __init__(self, date, fmt='%Y-%m-%d %H:%M:%S'):
        Date.__init__(self, date, fmt)

    def _apply(self, days=None, day=None, months=None, month=None, years=None,
               year=None, seconds=None, second=None, minutes=None, minute=None, hours=None, hour=None):
        Date._apply(self, days=days, months=months, years=years, day=day)
        date = datetime.strptime(self._date, self._fmt)
        if seconds is not None:
            date = date + relativedelta(seconds=seconds)
        if second is not None:
            date = date + relativedelta(second=second)
        if minutes is not None:
            date = date + relativedelta(minutes=minutes)
        if minute is not None:
            date = date + relativedelta(minute=minute)
        if hours is not None:
            date = date + relativedelta(hours=hours)
        if hour is not None:
            date = date + relativedelta(hour=hour)
        self._date = date.strftime(self._fmt)
        return self

    def next_second(self, seconds=1):
        return self._apply(seconds=seconds)

    def prev_second(self, seconds=1):
        return self._apply(seconds=-1 * seconds)

    def first_second_in_day(self):
        return self._apply(second=0, minute=0, hour=0)

    def last_second_in_day(self):
        return self._apply(second=59, minute=59, hour=23)

    def next_minute(self, minutes=1):
        return self._apply(minutes=minutes)

    def prev_minute(self, minutes=1):
        return self._apply(minutes=-1 * minutes)

    def next_hour(self, hours=1):
        return self._apply(hours=hours)

    def prev_hour(self, hours=1):
        return self._apply(hours=-1 * hours)


class DateRange:
    """docstring for DateRange"""

    def __init__(self, start, stop=False, exclude_weekdays=[], exclude_dates=[], fmt='%Y-%m-%d'):
        if isinstance(start, basestring):
            start = datetime.strptime(start, fmt)
        self._start = start
        if isinstance(stop, basestring):
            stop = datetime.strptime(stop, fmt)
        self._stop = stop
        self._exclude_dates = []
        if not hasattr(exclude_dates, '__iter__'):
            exclude_dates = [exclude_dates]
        for exclude_date in exclude_dates:
            if isinstance(exclude_date, basestring):
                exclude_date = datetime.strptime(exclude_date, fmt)
            self._exclude_dates.append(exclude_date)
        self._exclude_weekdays = []
        if not hasattr(exclude_weekdays, '__iter__'):
            exclude_weekdays = [exclude_weekdays]
        for exclude_weekday in exclude_weekdays:
            if isinstance(exclude_weekday, basestring):
                exclude_weekday = int(exclude_weekday)
            self._exclude_weekdays.append(exclude_weekday)
        self._fmt = fmt

    def __str__(self):
        return "(%s - %s) exclude dates %s and weekedays %s" % (
            self._start, self._stop, self._exclude_dates, self._exclude_weekdays)

    def __iter__(self):
        while not self._stop or self._start <= self._stop:
            if self._start.weekday() not in self._exclude_weekdays:
                if self._start not in self._exclude_dates:
                    yield self._start.strftime("%Y-%m-%d")
            self._start = self._start + relativedelta(days=1)
