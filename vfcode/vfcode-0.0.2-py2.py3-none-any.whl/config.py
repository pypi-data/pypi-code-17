# -*- coding: utf-8 -*-

"""
验证码配置类.
"""

from collections import namedtuple
import os
import pathlib
import string
import better_exceptions
from .utils import init_fonts_path, check_parameter


Width = namedtuple("Width", "min_width, max_width")
Height = namedtuple("Height", "min_height, max_height")
GradientColors = namedtuple("GradientColors", "min_gradient_colors, max_gradient_colors")
CharNum = namedtuple("CharNum", "min_charNum, max_charNum")

# 验证码字符字典
NUM = string.digits
LOWERCASE_CHAR = string.ascii_lowercase
UPPERCASE_CHAR = string.ascii_uppercase
CHAR = string.ascii_letters
NUM_CHAR = "".join([string.digits, string.ascii_letters])
CALCU_OPERATION = "+-x"

class Config(object):
    """验证码配置类."""

    def __init__(self):
        """默认配置."""
        # 验证码尺寸范围
        self.width = Width(100, 120)
        self.height = Height(25, 45)
        # 验证码图片背景渐变元色数目,也可以设置为单色背景
        self.gradient_colors = GradientColors(3, 6)
        # 验证码字符个数
        self.charNum = CharNum(4, 6)
        # 验证码字典
        self.char = NUM_CHAR
        # 中文验证码字符出现的概率,可以为0
        self.chinese_rate = 0.1
        # 设置字体路径
        self.fonts_path = init_fonts_path()
        # 验证码字符旋转最大角度,为0表示不旋转
        self.rotate_angle = 40
        # 噪声类型
        self.noises = ["point", "line", "circle"]
        # 验证码内容为算术题的概率
        self.calculation_rate = 0.2
        # 算术题操作类型
        self.calcu_operation = CALCU_OPERATION

    @check_parameter
    def setWidth(self, fixed_width=None, min_width=None, max_width=None):
        """设置验证码图片宽度范围.

        :param fixed_width: 设置验证码图片的固定宽度,如果不设置则使用宽度范围中的随机宽度.
        :param min_width: 设置验证码图片的最小宽度.
        :param max_width: 设置验证码图片的最大宽度.
        """
        if fixed_width is not None:
            self.width = Width(fixed_width, fixed_width)
        else:
            self.width = Width(min_width, max_width)

    @check_parameter
    def setHeight(self, fixed_height=None, min_height=None, max_height=None):
        """设置验证码图片长度范围.

        :param fixed_height: 设置验证码图片的固定长度,如果不设置则使用长度范围中的随机长度.
        :param min_height: 设置验证码图片的最小长度.
        :param max_height: 设置验证码图片的最大长度.
        """
        if fixed_height is not None:
            self.height = Height(fixed_height, fixed_height)
        else:
            self.height = Height(min_height, max_height)

    @check_parameter
    def setGradientColors(self, fixed_gradient_colors=None, min_gradient_colors=None, max_gradient_colors=None):
        """设置验证码背景渐变元色数目范围.

        :param fixed_gradient_colors: 设置验证码固定背景颜色.类型为字符串
        :param min_gradient_colors: 设置验证码背景渐变元色最小数目.
        :param max_gradient_colors: 设置验证码背景渐变元色最大数目.
        """
        if fixed_gradient_colors is not None:
            self.gradient_colors = fixed_gradient_colors
        else:
            self.gradient_colors = GradientColors(min_gradient_colors, max_gradient_colors)

    @check_parameter
    def setCharNum(self, fixed_charNum=None, min_charNum=None, max_charNum=None):
        """设置验证码字符个数范围.

        :param fixed_charNum: 设置验证码图片的固定字符个数,如果不设置则使用范围中的随机个数.
        :param min_charNum: 设置验证码图片的最小字符个数.
        :param max_charNum: 设置验证码图片的最大字符个数.
        """
        if fixed_charNum is not None:
            self.charNum = CharNum(fixed_charNum, fixed_charNum)
        else:
            self.charNum = CharNum(min_charNum, max_charNum)

    def setChar(self, charDict=NUM_CHAR, chinese_rate=0.25):
        """设置验证码字符字典,以及确定是否需要中文字符.

        :param charDict:验证码字符字典,目前可选为:
        config.NUM : '0123456789'
        config.LOWERCASE_CHAR : 'abcdefghijklmnopqrstuvwxyz'
        config.UPPERCASE_CHAR : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        config.CHAR : 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        config.NUM_CHAR : '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        也可以自己设置验证码字符取值字典,类型如以上的字符串
        :param chinese_rate: 中文验证码字符出现的概率,0表示不使用中文
        """
        self.char = charDict
        self.chinese_rate = chinese_rate

    def setFontsPath(self, en_fonts_path=None, ch_fonts_path=None):
        """设置字体路径.

        :param en_fonts_path:设置英文字体路径.可以是文件夹也可以是文件路径.
        :param ch_fonts_path:设置中文字体路径.可以是文件夹也可以是文件路径.
        """
        if en_fonts_path is not None:
            en_path = pathlib.Path(en_fonts_path)
            if en_path.is_dir():
                self.fonts_path.update({"en":list(en_path.iterdir())})
            else:
                self.fonts_path.update({"en":en_path})

        if ch_fonts_path is not None:
            ch_path = pathlib.Path(ch_fonts_path)
            if ch_path.is_dir():
                self.fonts_path.update({"ch":list(ch_path.iterdir())})
            else:
                self.fonts_path.update({"ch":ch_path})

    def setRotateAngle(self, rotate_angle=30):
        """设置验证码字符最大旋转角度.

        :param rotate_angle: 验证码字符最大旋转角度,为0表示不旋转
        """
        self.rotate_angle = rotate_angle

    def setNoises(self, noises):
        """设置噪声类型.

        :param noises: 噪声类型
        """
        if isinstance(noises, str):
            noises = [noises]
        self.noises = noises

    @check_parameter
    def setCalculationRate(self, calculation_rate):
        """设置验证码中出现算术题的概率.

        :param calculation_rate: 验证码中出现算术题的概率.
        """
        self.calculation_rate = calculation_rate

    def setCalcuOperation(self, calcu_operation):
        """设置算术题计算类型.

        :param calcu_operation：算术题计算类型.
        """
        self.calcu_operation = calcu_operation