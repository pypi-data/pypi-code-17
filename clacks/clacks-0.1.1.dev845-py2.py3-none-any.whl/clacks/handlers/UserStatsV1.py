#!/usr/bin/env python3

"""AdminUserStats class."""

import datetime

import cherrypy
from sqlalchemy import func

from ..db import db
from ..models import User, UserLog
from ..tools import range_from_header

from .URLHandler import URLHandler


class AdminUserStats(URLHandler):

    """AdminUserStats class."""

    mount_url = '/_v1/user-stats/'

    @cherrypy.expose
    @cherrypy.tools.require(grant='LOGIN_HISTORY_VIEW')
    def index(self):
        """There's nothing to be shown as index"""
        return ''

    @cherrypy.expose
    @cherrypy.tools.require(grant='LOGIN_HISTORY_VIEW')
    @cherrypy.tools.json_out()
    def daily_logins(self, **kwargs):

        """Return daily logins statistics."""

        maxDate = datetime.datetime.now().date()+datetime.timedelta(days=1)
        try:
            fromDate = datetime.datetime.strptime(kwargs.get("from", ""), "%Y-%m-%d").date()
        except ValueError:
            fromDate = datetime.date(1970, 1, 1)
        try:
            toDate = (datetime.datetime.strptime(kwargs.get("to", ""), "%Y-%m-%d").date() +
                      datetime.timedelta(days=1))
        except ValueError:
            toDate = maxDate

        if toDate > maxDate:
            toDate = maxDate
        if fromDate > (toDate-datetime.timedelta(days=7)):
            fromDate = toDate-datetime.timedelta(days=7)
        elif fromDate < (toDate-datetime.timedelta(days=365)):
            fromDate = toDate-datetime.timedelta(days=365)

        dfunc = func.date_trunc('day', UserLog.timestamp).label('date')

        dquery = db.query(func.generate_series(fromDate, toDate, '24 hours').label('date')).subquery()

        lquery = (db.query(dfunc, func.count(UserLog.timestamp).label('logins'))
                  .filter(UserLog.timestamp > fromDate, UserLog.timestamp < toDate)
                  .group_by(dfunc).subquery())

        series = (db.query(dquery.c.date, lquery.c.logins)
                  .outerjoin(lquery, dquery.c.date == lquery.c.date).order_by(dquery.c.date))

        return [{'id': round(d.timestamp()), 'logins': cnt or 0}
                for (d, cnt) in series[range_from_header(db.query(dquery).count())]]

    @cherrypy.expose
    @cherrypy.tools.require(grant='LOGIN_HISTORY_VIEW')
    @cherrypy.tools.json_out()
    def daily_registrations(self, **kwargs):

        """Registrations per day statistics"""

        maxDate = datetime.datetime.now().date()+datetime.timedelta(days=1)
        try:
            fromDate = datetime.datetime.strptime(kwargs.get('from', ''), '%Y-%m-%d').date()
        except ValueError:
            fromDate = datetime.date(1970, 1, 1)
        try:
            toDate = (datetime.datetime.strptime(kwargs.get('to', ''), '%Y-%m-%d').date() +
                      datetime.timedelta(days=1))
        except ValueError:
            toDate = maxDate

        if toDate > maxDate:
            toDate = maxDate
        if fromDate > (toDate-datetime.timedelta(days=7)):
            fromDate = toDate-datetime.timedelta(days=7)
        elif fromDate < (toDate-datetime.timedelta(days=365)):
            fromDate = toDate-datetime.timedelta(days=365)

        dfunc = func.date_trunc('day', User.created).label('date')

        dquery = db.query(func.generate_series(fromDate, toDate, '24 hours').label('date')).subquery()

        lquery = (db.query(dfunc, func.count(User.created).label('registrations'))
                  .filter(User.created > fromDate, User.created < toDate)
                  .group_by(dfunc).subquery())

        series = (db.query(dquery.c.date, lquery.c.registrations)
                  .outerjoin(lquery, dquery.c.date == lquery.c.date).order_by(dquery.c.date))

        return [{'id': round(d.timestamp()), 'registrations': cnt or 0}
                for (d, cnt) in series[range_from_header(db.query(dquery).count())]]

    @cherrypy.expose
    @cherrypy.tools.require(grant='LOGIN_HISTORY_VIEW')
    @cherrypy.tools.json_out()
    def day_cycle_logins(self, **kwargs):

        """Logins frequency per hour."""

        maxDate = datetime.datetime.now().date()+datetime.timedelta(days=1)
        try:
            fromDate = datetime.datetime.strptime(kwargs.get('from', ''), '%Y-%m-%d').date()
        except ValueError:
            fromDate = datetime.date(1970, 1, 1)
        try:
            toDate = (datetime.datetime.strptime(kwargs.get('to', ''), '%Y-%m-%d').date() +
                      datetime.timedelta(days=1))
        except ValueError:
            toDate = maxDate

        if toDate > maxDate:
            toDate = maxDate
        if fromDate > (toDate-datetime.timedelta(days=7)):
            fromDate = toDate-datetime.timedelta(days=7)
        elif fromDate < (toDate-datetime.timedelta(days=365)):
            fromDate = toDate-datetime.timedelta(days=365)

        dfunc = func.extract('hour', UserLog.timestamp).label('hour')

        dquery = db.query(func.generate_series(0, 23).label('hour')).subquery()

        lquery = (db.query(dfunc, func.count(UserLog._user).label('logins'))
                  .filter(UserLog.timestamp > fromDate, UserLog.timestamp < toDate)
                  .group_by(dfunc).subquery())

        series = (db.query(dquery.c.hour, lquery.c.logins)
                  .outerjoin(lquery, dquery.c.hour == lquery.c.hour).order_by(dquery.c.hour))

        return [{'id': d, 'logins': cnt or 0}
                for (d, cnt) in series[range_from_header(db.query(dquery).count())]]

    @cherrypy.expose
    @cherrypy.tools.require(grant='LOGIN_HISTORY_VIEW')
    @cherrypy.tools.json_out()
    def week_cycle_logins(self, **kwargs):

        """Logins frequency per day of week."""

        maxDate = datetime.datetime.now().date()+datetime.timedelta(days=1)
        try:
            fromDate = datetime.datetime.strptime(kwargs.get('from', ''), '%Y-%m-%d').date()
        except ValueError:
            fromDate = datetime.date(1970, 1, 1)
        try:
            toDate = (datetime.datetime.strptime(kwargs.get('to', ''), '%Y-%m-%d').date() +
                      datetime.timedelta(days=1))
        except ValueError:
            toDate = maxDate

        if toDate > maxDate:
            toDate = maxDate
        if fromDate > (toDate-datetime.timedelta(days=7)):
            fromDate = toDate-datetime.timedelta(days=7)
        elif fromDate < (toDate-datetime.timedelta(days=365)):
            fromDate = toDate-datetime.timedelta(days=365)

        dfunc = func.extract('dow', UserLog.timestamp).label('dow')

        dquery = db.query(func.generate_series(0, 6).label('dow')).subquery()

        lquery = (db.query(dfunc, func.count(UserLog._user).label('logins'))
                  .filter(UserLog.timestamp > fromDate, UserLog.timestamp < toDate)
                  .group_by(dfunc).subquery())

        series = (db.query(dquery.c.dow, lquery.c.logins)
                  .outerjoin(lquery, dquery.c.dow == lquery.c.dow).order_by(dquery.c.dow))

        return [{'id': d, 'logins': cnt or 0}
                for (d, cnt) in series[range_from_header(db.query(dquery).count())]]
