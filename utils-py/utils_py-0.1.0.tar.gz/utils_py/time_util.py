#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Yitian Jia <ytjia.zju@gmail.com>

import datetime
import time


def ts_to_dt_str(ts, dt_format='%Y-%m-%d %H:%M:%S'):
    """
    时间戳转换为日期字符串
    Args:
        ts: 待转换的时间戳
        dt_format: 目标日期字符串格式

    Returns: 日期字符串

    """
    return datetime.datetime.fromtimestamp(int(ts)).strftime(dt_format)


def str_to_datetime(dt_str, fmt='%Y-%m-%d %H:%M:%S'):
    """
    字符串转换为datetime类型数据
    :param dt_str:
    :param fmt:
    :return:
    """
    d_time = datetime.datetime.strptime(dt_str, fmt)
    return d_time


def ts_to_datetime(ts):
    """
    时间戳转换为datetime
    :param ts: timestamp
    :return: datetime
    """
    d_time = datetime.datetime.fromtimestamp(int(ts))
    return d_time


def dt_to_ts(dt):
    """
    datetime转换为时间戳
    :param dt: datetime
    :return:
    """
    return int(time.mktime(dt.timetuple()))


def dt_to_str(dt, fmt='%Y-%m-%d %H:%M:%S'):
    """
    datetime转换为字符串
    :param dt: datetime
    :param fmt: 字符串格式
    :return:
    """
    return dt.strftime(fmt)


def dt_delta(dt, delta):
    """
    获取dt相隔delta的日期
    :param dt:
    :param delta:
    :return:
    """
    delta_time = datetime.timedelta(days=delta)
    target_date = dt + delta_time
    return target_date


def time_str_to_minutes(time_str):
    """
    通过时间字符串计算得到这是一天中第多少分钟
    :param time_str: eg: '11:10:00'
    :return: int
    """
    time_arr = time_str.split(":")
    hours = int(time_arr[0])
    minutes = int(time_arr[1])
    return hours * 60 + minutes


def minutes_to_time_str(mm_of_day):
    """
    将一天中第x分钟信息转换为hh:mm:ss格式的字符串
    eg: 0 -> 00:00:00, 61 -> 01:01:00
    :param mm_of_day: 一天中第x分钟
    :return: hh:mm:ss格式的字符串
    """
    hour = mm_of_day / 60
    minute = mm_of_day % 60
    return '{:0>2}:{:0>2}:{:0>2}'.format(hour, minute, 0)


def get_minutes_of_day(dt):
    """
    计算datetime时刻是一天中第多少分钟
    :param dt:
    :return:
    """
    return dt.hour * 60 + dt.minute


def today_dt_str():
    """
    获取系统时间今天的日期str，格式'%Y-%m-%d'
    :return:
    """
    now_ts = time.time()
    return ts_to_dt_str(now_ts, '%Y-%m-%d')


if __name__ == '__main__':
    today = today_dt_str()
    today_dt = str_to_datetime(today, '%Y-%m-%d')
    print(today)
    print(today_dt)
    print(dt_delta(today_dt, 1))
    print(ts_to_dt_str(1478016000, '%H:%M'))
