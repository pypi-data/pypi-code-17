# -*- coding: utf-8 -*-

"""
vfcode.utils
~~~~~~~~~~~~

This module provides utility functions that are used within vfcode
that are also useful for external consumption.
"""

import functools
import inspect
import os
import pathlib
import random
import sys
import better_exceptions


def get_vfcode_path():
    """
    获取vfcode的绝对路径.

    :rtype: pathlib.Path()
    """
    return pathlib.Path(os.path.realpath(sys.modules["vfcode"].__file__)).parent

def init_fonts_path():
    """
    初始化字体路径,目前字体文件夹有中文字体和英文字体.

    :rtype: {"ch":[fontpath, fontpath...], "en":[fontpath, fontpath...]...}
    """
    fonts_path_dict = {}
    fonts_absolute_path = get_vfcode_path() / "fonts"
    for fonts_country in fonts_absolute_path.iterdir():
        fonts_path = []
        for font in fonts_country.iterdir():
            fonts_path.append(str(font))
        fonts_path_dict[fonts_country.name] = fonts_path
    return fonts_path_dict

def randRGB():
    """
    返回一个随机rgb颜色组合.

    :rtype: (r, g, b)
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randChinese():
    """从gb2312国标一级汉字中随机生成汉字."""
    head = random.randint(0xB0, 0xCF)
    body = random.randint(0xA, 0xF)
    tail = random.randint(0, 0xF)
    val = ( head << 8 ) | (body << 4) | tail
    str = "%x" % val
    return bytes().fromhex(str).decode("gb2312")

def check_parameter(f):
    """装饰器: 检测函数参数是否大于0,若小于等于0,则报错."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        func_args = inspect.getcallargs(f, *args, **kwargs)
        for arg,value in func_args.items():
            if isinstance(value, int):
                if value < 0:
                    raise Exception(arg + "不能小于0")
        return f(*args, **kwargs)
    return wrapper
