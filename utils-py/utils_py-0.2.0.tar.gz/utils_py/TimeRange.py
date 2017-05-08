#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Yitian Jia <ytjia.zju@gmail.com>


import time_util


class TimeRange:
    """
    时间区间
    属性：区间起始datetime，终止datetime
    """

    def __init__(self, time_range_str, time_fmt='%Y-%m-%d %H:%M:%S'):
        [begin_time_str, end_time_str] = time_range_str.split('-')
        self.begin_dt = time_util.str_to_datetime(begin_time_str, time_fmt)
        self.end_dt = time_util.str_to_datetime(end_time_str, time_fmt)

    def lie_between(self, target_time_range):
        """
        判断是否落在目标时间区间内
        :param target_time_range: 目标时间区间
        :return: True or False
        """
        if self.begin_dt >= target_time_range.begin_dt and self.end_dt <= \
                target_time_range.end_dt:
            return True
        else:
            return False

    def do_intersect(self, another_time_range):
        """
        判断与另一时间区间是否有重叠
        :param another_time_range:
        :return: True or False
        """
        if self.begin_dt > another_time_range.end_dt or self.end_dt < \
                another_time_range.begin_dt:
            return False
        else:
            return True
