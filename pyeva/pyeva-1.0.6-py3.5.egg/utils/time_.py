#!/usr/bin/env python
# coding: utf-8

import time
import datetime
import dateutil


def htime( t ):

    ''' return a human ago aime '''

    if not isinstance(t, datetime.datetime):
        return 'N/A'

    ago = dateutil.relativedelta.relativedelta(datetime.datetime.now(), t)

    if ago.years > 0:
        s = u'%s年前' % ago.years

    elif ago.months > 0:
        s = u'%s月前' % ago.months

    elif ago.days > 0:
        s = u'%s天前' % ago.days

    elif ago.hours > 0:
        s = u'%s小时前' % ago.hours

    elif ago.minutes > 0:
        s = u'%s分钟前' % ago.minutes

    elif ago.seconds > 0:
        s = u'%s秒前' % ago.seconds

    else:
        #s = _('%s microseconds ago') % ago.microseconds
        s = u'刚刚'

    return s


def ftime(t, f='%Y-%m-%d %H:%M:%S'):

    try:
        return datetime.datetime.strftime(t, f)
    except:
        return 'N/A'


def after_days(days):

    '''返回指定天数后的时间

    '''

    now = datetime.datetime.utcnow()
    return now + datetime.timedelta(days=days)


def after_seconds(seconds):

    '''返回指定秒数后的时间

    '''

    now = datetime.datetime.utcnow()
    return now + datetime.timedelta(seconds=seconds)


def seconds(dt):

    '''转换 datetime 时间为秒（UNIX）
    '''
    if dt:
        return int(time.mktime(dt.timetuple()))
    else:
        return 0


def dt(seconds):
    '''转换 UNIX timestamp 为 datetime 对象
    '''
    return datetime.datetime.fromtimestamp(seconds)


def rfc3339_string(t):
    '''转化 datetime 为 rfc3339 格式字符串'''
    if isinstance(t, datetime.datetime):
        return t.isoformat('T') + 'Z'
