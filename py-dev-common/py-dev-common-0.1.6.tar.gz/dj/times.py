from datetime import datetime, timedelta

import pytz
from django.conf import settings

from django.utils import timezone

local_tz = pytz.timezone(settings.TIME_ZONE)


def from_timestamp(time):
    return timezone.make_aware(datetime.fromtimestamp(time))


def utc2local(dt):
    """
    将数据库读取的时间字符串转为本地时间
    """
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=local_tz)


def localtime(dt):
    if isinstance(dt, datetime):
        try:
            return dt.astimezone(tz=local_tz)
        except ValueError:
            return local_tz.localize(dt)
    return dt


def convert_timezone(time_in):
    """
    用来将系统自动生成的datetime格式的utc时区时间转化为本地时间
    :param time_in: datetime.datetime格式的utc时间
    :return:输出仍旧是datetime.datetime格式，但已经转换为本地时间
    """
    # time_utc = time_in.replace(tzinfo=timezone.utc)
    # time_local = time_utc.astimezone(local_tz)
    # return time_local
    return utc2local(time_in)


def to_str(date, fmt='%Y-%m-%d %H:%M'):
    if not date:
        return ''
    return localtime(date).strftime(fmt)


def to_pecker_str(date, fmt='%Y%m%d%H%M%S'):
    return to_str(date, fmt)


def to_date_str(date, fmt='%Y-%m-%d'):
    return to_str(date, fmt)


def friend_date(date, fmt='%m.%d'):
    if not date:
        return ''

    today = localtime(timezone.now()).date()
    if isinstance(date, datetime):
        date = localtime(date).date()

    if date == today:
        return '今天'
    elif date > today - timedelta(days=1):
        return '昨天'
    else:
        return to_date_str(date, fmt)


def to_datetime(time):
    return timezone.datetime.fromtimestamp(time, tz=timezone.get_default_timezone())
