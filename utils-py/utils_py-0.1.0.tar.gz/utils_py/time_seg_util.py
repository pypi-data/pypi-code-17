#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Yitian Jia <jiayitian@didichuxing.com>

import const
import time_util


def gen_slide_seg_list(mm_begin, mm_end, seg_duration, slide_step):
    """
    生成时间片开始时刻列表,时间片以slide_step步长进行滑动
    :param mm_begin:
    :param mm_end:
    :param seg_duration:
    :param slide_step:
    :return:
    """
    seg_begin_list = [i for i in
                      range(mm_begin, mm_end - seg_duration + 1, slide_step)]
    seg_list = map(time_util.minutes_to_time_str, seg_begin_list)
    return seg_list


def gen_still_seg_list(mm_begin, mm_end, seg_duration):
    """
    生成一段时间内的非滑动时间窗口列表
    :param mm_begin:
    :param mm_end:
    :param seg_duration: 时间片长度
    :return:
    """
    return gen_slide_seg_list(mm_begin, mm_end, seg_duration, seg_duration)


def get_slide_seg_list_belonged(dt_str, seg_duration, slide_step=1,
                                fmt='%Y-%m-%d %H:%M:%S'):
    """
    获取该时刻所属的所有时间片列表
    :param dt_str: datetime string, eg: 2016-10-31 12:22:11
    :param seg_duration: 时间片长度, unit: minute
    :param slide_step: 滑动步长
    :param fmt: datetime string format
    :return: 时间片列表
    """
    dt = time_util.str_to_datetime(dt_str, fmt)
    day_slide_seg_list = gen_slide_seg_list(
            const.FIRST_MINUTE_OF_DAY, const.MINUTES_IN_A_DAY, seg_duration,
            slide_step)
    return filter(lambda x: lie_in_seg(dt, x, seg_duration), day_slide_seg_list)


def get_still_seg_belonged(dt_str, seg_duration, fmt='%Y-%m-%d %H:%M:%S'):
    """
    获取该时刻所属的非滑动时间片
    :param dt_str: datetime string, eg: 2016-10-31 12:22:11
    :param seg_duration: 时间片长度, unit: minute
    :param fmt: datetime string format
    :return:
    """
    dt = time_util.str_to_datetime(dt_str, fmt)
    minutes_of_day = time_util.get_minutes_of_day(dt)
    return time_util.minutes_to_time_str(
            minutes_of_day - minutes_of_day % seg_duration)


def lie_in_seg(dt, time_str, seg_duration):
    """
    判断datetime是否在time_str为起点的时间片内
    :param dt:
    :param time_str: eg: '11:10:21'
    :param seg_duration:
    :return:
    """
    minutes_of_day = time_util.get_minutes_of_day(dt)
    range_begin = time_util.time_str_to_minutes(time_str)
    if range_begin <= minutes_of_day < range_begin + seg_duration:
        return True
    else:
        return False


def time_seg_to_index(time_str, slide_step):
    """
    将时间片字符串转换为时间片索引值
    :param time_str: eg: '11:10:21'
    :param slide_step:
    :return:
    """
    minutes_idx = time_util.time_str_to_minutes(time_str)
    time_seg_idx = minutes_idx // slide_step
    return time_seg_idx


def index_to_time_seg(time_seg_idx, slide_step):
    """
    将时间片索引值转换为时间片字符串
    :param time_seg_idx:
    :param slide_step:
    :return:
    """
    assert (time_seg_idx * slide_step < const.MINUTES_IN_A_DAY)
    return time_util.minutes_to_time_str(time_seg_idx * slide_step)


if __name__ == '__main__':
    print(get_slide_seg_list_belonged('2016-11-01 00:24:00', seg_duration=30,
                                      slide_step=7))
    print(get_slide_seg_list_belonged('2016-11-01 23:51:00', seg_duration=30))

    print(lie_in_seg(time_util.str_to_datetime(
            time_util.today_dt_str(), fmt='%Y-%m-%d'), '00:10:00', 30))
