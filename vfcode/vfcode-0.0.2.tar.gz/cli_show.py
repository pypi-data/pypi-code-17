# -*- coding: utf-8 -*-

"""
命令行抗识别验证码生成工具.

usage:
"""

import string
import better_exceptions
import click
import vfcode


NUM_CHAR = "".join([string.digits, string.ascii_letters])
vfcode_path = vfcode.utils.get_vfcode_path()

@click.command()
@click.option('--min_width', default=100, help='验证码图片最小长度')
@click.option('--max_width', default=120, help='验证码图片最大长度')
@click.option('--min_height', default=25, help='验证码图片最小高度')
@click.option('--max_height', default=45, help='验证码图片最大高度')
@click.option('--min_charnum', default=4, help='验证码字符最小数目')
@click.option('--max_charnum', default=6, help='验证码字符最大数目')
@click.option('--chardict', default=NUM_CHAR, help='验证码字符取值字典')
@click.option('--chinese_rate', default=0.1, help='验证码中出现中文字符的概率')
@click.option('--en_fonts_path', default=str(vfcode_path / "fonts/en"), help='英文字体目录或文件路径')
@click.option('--ch_fonts_path', default=str(vfcode_path / "fonts/ch"), help='中文字体目录或文件路径')
@click.option('--rotate_angle', default=40, help='验证码字符最大旋转角度')
@click.option('--noises', default=['point','line','circle'], help='验证码噪声类型')
@click.option('--calculation_rate', default=0.2, help='验证码为算术型验证码的概率')
@click.option('--calcu_operation', default="+-x", help='验证码算术类型')
@click.option('--gradient_colors', default="3,6", help='验证码背景图渐变元色')
@click.option('--save_path', default=None, help='验证码图片保存位置')
def generate(min_width, max_width, min_height, max_height, min_charnum, max_charnum,
             chardict, chinese_rate, en_fonts_path, ch_fonts_path, rotate_angle, noises,
             calculation_rate, calcu_operation, gradient_colors, save_path):
    """验证码生成器."""

    config = vfcode.Config()

    # 验证码长度范围设置
    config.setWidth(min_width=min_width, max_width=max_width)

    # 验证码高度范围设置
    config.setHeight(min_height=min_height, max_height=max_height)

    # 验证码字符个数设置
    config.setCharNum(min_charNum=min_charnum, max_charNum=max_charnum)

    # 验证码字符字典设置
    config.setChar(charDict=chardict, chinese_rate=chinese_rate)

    # 验证码字体路径设置
    config.setFontsPath(en_fonts_path=en_fonts_path, ch_fonts_path=ch_fonts_path)

    # 验证码字符最大旋转角度
    config.setRotateAngle(rotate_angle=rotate_angle)

    # 验证码噪声类型设置
    config.setNoises(noises=noises)

    # 验证码出现算术题的概率设置
    config.setCalculationRate(calculation_rate=calculation_rate)

    # 验证码算术题操作类型设置
    config.setCalcuOperation(calcu_operation=calcu_operation)

    # 验证码渐变颜色设置
    if "," in gradient_colors:
        min_gradient_colors = int(gradient_colors.split(",")[0])
        max_gradient_colors = int(gradient_colors.split(",")[1])
        config.setGradientColors(min_gradient_colors=min_gradient_colors, max_gradient_colors=max_gradient_colors)
    else:
        config.setGradientColors(fixed_gradient_colors=gradient_colors)


    gener = vfcode.Generator(config=config)

    image, chars, path = gener.generate(save_path=save_path)
    print("生成的验证码为: " + "".join(chars))
    print("验证码图片路径为: " + path)

if __name__ == '__main__':
    generate()