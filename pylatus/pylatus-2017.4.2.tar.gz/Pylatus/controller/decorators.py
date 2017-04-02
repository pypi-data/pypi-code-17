#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


def customable(func):
    def wrapper(*args, **kwargs):
        scope = sys._getframe().f_back.f_code.co_name
        if scope != '<module>':
            kwargs['now'] = True
        return func(*args, **kwargs)
    return wrapper


def split_motor_name(func):
    def wrapper(*args, **kwargs):
        if len(args) >= 1:
            args = list(args)
            if isinstance(args[1], str) and '->' in args[1]:
                args[1] = args[1].split('->')[-1]
        return func(*args, **kwargs)
    return wrapper
