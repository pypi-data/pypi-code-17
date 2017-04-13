#!/usr/bin/env python
# coding: utf-8

"""My python util"""


from contextlib import contextmanager as cm
import logging

import decorator

__author__ = 'Meme Kagurazaka (神楽坂爻)'
__license__ = 'Public Domain'
__version__ = 'v0.0.1'


def get_abbreviation(s):
    """Acronym and abbreviation used in this module"""
    return {
        'f': 'function',
        'func': 'function',
        'lvl': 'level',
    }[s]


@cm
def let(*args):
    """the let"""
    yield args[0] if len(args == 1) else args


def deprecated(func_name=None, log_lvl=logging.WARNING):
    """Label deprecated functions"""
    @decorator.decorator
    def _(f, *args, **kw):
        logging.log(log_lvl, "%s is deprecated", func_name if func_name else f)
        return f(*args, **kw)
    return _
