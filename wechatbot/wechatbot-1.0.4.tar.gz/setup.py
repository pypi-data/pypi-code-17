# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))


entry_points = [
    "wechatbot = wechatbot.bot:main"
]

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name="wechatbot",
    version='1.0.4',
    description="a wechat bot developed for geeks",
    long_description=long_description,
    author="chuanwu",
    author_email="chuanwusun@gmail.com",
    keywords="wechat bot chatops",
    packages=['wechatbot'],
    license='MIT',
    url="https://github.com/chuanwu/WechatBot.py",
    entry_points={"console_scripts": entry_points},
    install_requires=[],

)
