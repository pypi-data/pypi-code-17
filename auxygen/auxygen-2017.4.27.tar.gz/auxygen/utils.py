#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math


DEFAULT_TIMEOUT = 3000
DEFAULT_ERROR = 0.5


def split_motor_name(func):
    def wrapper(*args, **kwargs):
        if len(args) >= 1:
            args = list(args)
            if isinstance(args[1], str) and '->' in args[1]:
                args[1] = args[1].split('->')[-1]
        return func(*args, **kwargs)
    return wrapper


def customable(func):
    def wrapper(*args, **kwargs):
        scope = sys._getframe().f_back.f_code.co_name
        if scope != '<module>':
            kwargs['now'] = True
        return func(*args, **kwargs)
    return wrapper


def calcTime(uptime):
    if uptime < 60:
        days, hours, minutes = 0, 0, int(math.floor(uptime))
    elif 60 <= uptime < 60 * 24:
        hours = int(uptime // 60)
        minutes = int(math.floor(uptime - hours * 60))
        days = 0
    else:
        days = int(uptime // (60 * 24))
        hours = int(uptime // 60 - days * 24)
        minutes = int(math.floor(uptime - days * 60 * 24 - hours * 60))
    return days, hours, minutes


def pyqt2bool(entry):
    return not (entry == 'false' or not entry)
