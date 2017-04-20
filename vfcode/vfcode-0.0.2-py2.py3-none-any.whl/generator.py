# -*- coding: utf-8 -*-

"""
验证码生成器.
"""

import hashlib
import os
import pathlib
import random
import string
import arrow
import better_exceptions
from PIL import Image, ImageDraw, ImageFont
from .config import Config
from .import render
from .utils import randChinese, randRGB

class Generator(object):
    """验证码生成器."""

    def __init__(self, config=None):
        """为验证码生成器设置验证码配置类.

        :param config:验证码配置类,若为空,则使用默认的配置类
        """
        if config is not None:
            self.config = config
        else:
            self.config = Config()

    def generate(self, save_path=None):
        """生成单张验证码图片.

        :param save_path: 验证码图片保存位置.
        当路径为文件夹时,以时间戳md5为名称保存验证码图片在该目录下;
        当路径为图片文件名时,保存在当前工作路径下;
        当路径为空时,以时间戳md5为名称保存验证码图片在当前工作目录下.
        :rtype: (image, CAPTCHA, image_path) CAPTCHA为验证码字符,image_path为验证码图片绝对路径.
        """
        # 生成随机大小的背景
        image = self.create_image(self.config)
        # 背景图渐变处理
        if not isinstance(self.config.gradient_colors, str) and self.config.gradient_colors.max_gradient_colors > 1:
            image = render.gradient(image, self.config)

        # 选取随机个数的验证码字符,包括算术题的情况
        captchas, is_calcu = self.random_char(self.config)

        if not is_calcu:
            # 将每个验证码字符绘制到背景图片上
            for i in range(len(captchas)):
                captcha_size = random.randint(image.height - 10, image.height)
                captcha_image = Image.new(mode='RGBA', size=(captcha_size*2, captcha_size*2))
                if captchas[i] not in self.config.char:
                    font_path = random.sample(self.config.fonts_path.get("ch"), 1)
                else:
                    font_path = random.sample(self.config.fonts_path.get("en"), 1)
                font = ImageFont.truetype(str(font_path[0]), captcha_size)
                drawer = ImageDraw.Draw(captcha_image)
                drawer.text(xy=(0, 0), text=captchas[i], fill=randRGB(), font=font)
                if abs(self.config.rotate_angle) != 0:
                    captcha_image = render.rotate(captcha_image, self.config.rotate_angle)
                captcha_image = captcha_image.crop(captcha_image.getbbox())
                space = len(captchas) <= 4 and 10 or 20
                image.paste(captcha_image, (random.randint((image.width-space)//len(captchas) * i - 5, (image.width-10)//len(captchas) * i), random.randint(0, image.height - captcha_size)), captcha_image)

        # 验证码为算术题的情况
        else:
            for i in range(len(captchas)):
                captcha_size = random.randint(image.height - 15, image.height - 10)
                font_path = random.sample(self.config.fonts_path.get("en"), 1)
                font = ImageFont.truetype(str(font_path[0]), captcha_size)
                drawer = ImageDraw.Draw(image)
                drawer.text(xy=(i*captcha_size, random.randint(3, 5)), text=captchas[i], fill=randRGB(), font=font)

        # 绘制噪声
        image = render.noise(image, self.config)

        # 保存验证码图片
        time_now = arrow.now().timestamp
        md5 = hashlib.md5(str(time_now).encode("utf8")).hexdigest()
        if save_path is not None:
            if pathlib.Path(save_path).is_dir():
                save_path = save_path + os.path.sep + md5 + ".png"
                image.save(save_path)
            else:
                image.save(save_path)
        else:
            save_path = os.getcwd() + os.path.sep + md5 + ".png"
            image.save(save_path)

        if is_calcu:
            captchas = self.calcu_captcha(captchas)

        return (image, captchas, save_path)

    # 批量生成验证码
    def generate_many(self, num = 10, save_path=None):
        """批量生成验证码.

        :param num: 生成验证码的数目.
        :param svae_path: 验证码保存路径
        """
        for i in range(num):
            self.generate(save_path=save_path)

    def create_image(self, config):
        """创建验证码背景图片.

        :param config: 配置类.
        :rtype: Image
        """
        width = random.randint(config.width.min_width, config.width.max_width)
        height = random.randint(config.height.min_height, config.height.max_height)
        if isinstance(config.gradient_colors, str):
            image = Image.new(mode="RGBA", size=(width, height), color=config.gradient_colors)
        else:
            image = Image.new(mode="RGBA", size=(width, height), color=randRGB())
        return image

    def random_char(self, config):
        """随机选取验证码字符.

        :param config: 配置类.
        :rtype: (List, bool)
        """
        captchas = []
        if random.random() > config.calculation_rate:
            is_calcu = False
            charNum = random.randint(config.charNum.min_charNum, config.charNum.max_charNum)
            for i in range(charNum):
                if random.random() < config.chinese_rate:
                    try:
                        captchas.append(randChinese())
                    except Exception as e:
                        continue
                else:
                    captchas.append(random.sample(config.char, 1)[0])

        # 验证码为算术题的情况
        else:
            is_calcu = True
            captchas.append(str(random.randint(0, 99)))
            captchas.append(random.sample(config.calcu_operation, 1)[0])
            captchas.append(str(random.randint(0, 99)))
            captchas.append("=")
            captchas.append("?")
        return captchas, is_calcu

    def calcu_captcha(self, captchas):
        """当验证码为计算题的时候算出结果.

        :param captchas: 验证码字符.
        :rtype: int
        """
        if captchas[1] == "+":
            result = int(captchas[0]) + int(captchas[2])
        elif captchas[1] == "-":
            result = int(captchas[0]) - int(captchas[2])
        elif captchas[1] == "x":
            result = int(captchas[0]) * int(captchas[2])
        else:
            raise Exception("还未注册该算数操作,待程序更新")
        return str(result)

    def cha_draw(self, cha, text_color, font, rotate,size_cha):
        im = Image.new(mode='RGBA', size=(size_cha*2, size_cha*2))
        drawer = ImageDraw.Draw(im)
        drawer.text(xy=(0, 0), text=cha, fill=text_color, font=font) #text 内容，fill 颜色， font 字体（包括大小）
        if rotate:
            max_angle = 40 # to be tuned
            angle = random.randint(-max_angle, max_angle)
            im = im.rotate(angle, Image.BILINEAR, expand=1)
        im = im.crop(im.getbbox())
        return im

    def captcha_draw(self, size_im, nb_cha, set_cha, fonts=None, overlap=0.0,
        rd_bg_color=False, rd_text_color=False, rd_text_pos=False, rd_text_size=False,
        rotate=False, noise=None, dir_path='',img_num=0,img_now=0):

        rate_cha = 0.8 # rate to be tuned
        width_im, height_im = size_im
        width_cha = int(width_im / max(nb_cha-overlap, 5)) # 字符区域宽度
        height_cha = height_im*1.2# 字符区域高度
        bg_color = 'white'
        text_color = 'black'
        derx = 0
        dery = 0

        if rd_text_size:
            rate_cha = random.uniform(rate_cha-0.1, rate_cha+0.1) # to be tuned
        size_cha = int(rate_cha*min(width_cha, height_cha) * 2.0)# 字符大小

        if rd_bg_color:
            bg_color = randRGB()
        im = Image.new(mode='RGB', size=size_im, color=bg_color) # color 背景颜色，size 图片大小

        drawer = ImageDraw.Draw(im)
        contents = []
        for i in range(nb_cha):
            if rd_text_color:
                text_color = randRGB()
            if rd_text_pos:
                derx = random.randint(0, max(width_cha-size_cha-5, 0))
                dery = random.randint(0, max(height_cha-size_cha-5, 0))

            cha = random.choice(set_cha)
            font = ImageFont.truetype(fonts, size_cha)
            contents.append(cha)
            im_cha = self.cha_draw(cha, text_color, font, rotate, size_cha)
            im.paste(im_cha, (int(max(i-overlap, 0)*width_cha)+derx + 2, dery + 3), im_cha) # 字符左上角位置

        if 'point' in noise:
            nb_point = 20
            color_point = randRGB()
            for i in range(nb_point):
                x = random.randint(0, width_im)
                y = random.randint(0, height_im)
                drawer.point(xy=(x, y), fill=color_point)
        if 'line' in noise:
            nb_line = 3
            for i in range(nb_line):
                color_line = randRGB()
                sx = random.randint(0, width_im)
                sy = random.randint(0, height_im)
                ex = random.randint(0, width_im)
                ey = random.randint(0, height_im)
                drawer.line(xy=(sx, sy, ex, ey), fill=color_line)
        if 'circle' in noise:
            nb_circle = 20
            color_circle = randRGB()
            for i in range(nb_circle):
                sx = random.randint(0, width_im-10)
                sy = random.randint(0, height_im-10)
                temp = random.randint(1,5)
                ex = sx+temp
                ey = sy+temp
                drawer.arc((sx, sy, ex, ey), 0, 360, fill=color_circle)

        if not os.path.exists(dir_path): # 如果文件夹不存在，则创建对应的文件夹
            os.mkdir(dir_path)

        img_name = str(img_now) + '_' + ''.join(contents) + '.jpg'
        img_path = dir_path + "/" + img_name
        im.save(img_path)


    def cha_for_lstm(self):
        """生成用于训练的验证码."""
        size_im = (100, 30) # 图片大小
        overlaps = [0.0, 0.2, 0.4] # 字符之间区域可重叠百分比, 重叠效果和图片宽度字符宽度有关
        rd_text_poss = [False, True]
        rd_text_sizes = [False, True]
        rd_text_colors = [False, True] # false 代表字体颜色全一致，但都是黑色
        rd_bg_color = False
        set_chas = [self.const.NUM, self.const.CHAR, self.const.NUM_CHAR]
        noises = [ ['point'], ['line'], ['line', 'point'], ['circle'] ]
        rotates =[True, False]
        nb_chas = [6]
        font_paths = self.const.FONTS_PATH["en"]
        nb_image = 5000
        num_pic = 0
        dir_path = get_vfcode_path() / "../images_train"   # 用于存放训练图片的文件夹

        for i in range(nb_image):
            overlap = random.choice(overlaps)
            rd_text_pos = random.choice(rd_text_poss)
            rd_text_size = random.choice(rd_text_sizes)
            rd_text_color = random.choice(rd_text_colors)
            set_cha = random.choice(set_chas)
            noise = random.choice(noises)
            rotate = random.choice(rotates)
            nb_cha = random.choice(nb_chas)
            font_path = random.choice(font_paths)

            self.captcha_draw(size_im=size_im, nb_cha=nb_cha, set_cha=set_cha,
                overlap=overlap, rd_text_pos=rd_text_pos, rd_text_size=rd_text_size,
                rd_text_color=rd_text_color, rd_bg_color=rd_bg_color, noise=noise,
                rotate=rotate, dir_path=str(dir_path), fonts=str(font_path),img_num = nb_image,img_now = i)