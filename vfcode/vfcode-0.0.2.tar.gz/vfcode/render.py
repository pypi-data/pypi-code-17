# -*- coding: utf-8 -*-

"""
vfcode.render
~~~~~~~~~~~~

图片渲染器

目前支持的渲染操作:
1:
"""

import random
import better_exceptions
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .utils import randRGB


def rotate(image, rotate_angle):
    """字符旋转.

    :param image: 单个验证码字符图片
    :rtype: Image
    """
    angle = random.randint(-rotate_angle, rotate_angle)
    image = image.rotate(angle, Image.BILINEAR, expand=1)
    return image

def lerpColour(c1,c2,t):
    """渐变过渡算法.

    :param c1: 颜色1
    :param c2: 颜色2
    :param t: step
    :rtype: (R, G, B)
    """
    return (int(c1[0]+(c2[0]-c1[0])*t), int(c1[1]+(c2[1]-c1[1])*t), int(c1[2]+(c2[2]-c1[2])*t))


def gradient_colors(image, length, gradient_colors_num):
    """渐变元颜色.

    :param image: Image
    :param length: 决定横向渐变还是纵向渐变
    :param gradient_colors_num: 渐变元颜色数目
    :rtype: List((R, G, B), (R, G, B), (R, G, B),......)
    """
    list_of_colors = [randRGB() for i in range(gradient_colors_num)]

    no_steps = length // (gradient_colors_num - 1) + 1

    gradient = []
    for i in range(len(list_of_colors)-1):
        for j in range(no_steps):
            gradient.append(lerpColour(list_of_colors[i],list_of_colors[i+1],j/no_steps))
    return gradient

def gradient(image, config):
    """背景图渐变处理.

    :param image: Image
    :param config: 配置类.
    :rtype: Image
    """
    height = image.height
    width = image.width

    draw = ImageDraw.Draw(image)

    gradient_colors_num = random.randint(config.gradient_colors.min_gradient_colors, config.gradient_colors.max_gradient_colors)
    if gradient_colors_num == 0:
        image

    # 横向渐变和纵向渐变几率各为50%
    if random.random() > 0.5:
        list_of_colors = gradient_colors(image, width, gradient_colors_num)

        for i in range(width):
            draw.line((i, 0, i, height), fill=list_of_colors[i])
    else:
        list_of_colors = gradient_colors(image, height, gradient_colors_num)

        for i in range(height):
            draw.line((0, i, width, i), fill=list_of_colors[i])

    image = image.filter(ImageFilter.BLUR).filter(ImageFilter.SMOOTH_MORE)
    return image

def noise(image, config):
    """绘制噪声.

    :param image: Image
    :param config: 配置类.
    :rtype: Image
    """
    height = image.height
    width = image.width
    noises = config.noises
    drawer = ImageDraw.Draw(image)
    if 'point' in noises:
        nb_point = random.randint(10, 20)
        color_point = randRGB()
        for i in range(nb_point):
            x = random.randint(0, width)
            y = random.randint(0, height)
            drawer.point(xy=(x, y), fill=color_point)
    if 'line' in noises:
        nb_line = random.randint(3, 5)
        for i in range(nb_line):
            color_line = randRGB()
            sx = random.randint(0, width)
            sy = random.randint(0, height)
            ex = random.randint(0, width)
            ey = random.randint(0, height)
            drawer.line(xy=(sx, sy, ex, ey), fill=color_line)
    if 'circle' in noises:
        nb_circle = random.randint(3, 5)
        color_circle = randRGB()
        for i in range(nb_circle):
            sx = random.randint(0, width-10)
            sy = random.randint(0, height-10)
            temp = random.randint(1,5)
            ex = sx+temp
            ey = sy+temp
            drawer.arc((sx, sy, ex, ey), 0, 360, fill=color_circle)

    return image
