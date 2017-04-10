# -*- coding: utf-8 -*-

from setuptools import setup

entry_points = [
    "wechatbot = wechatbot.wechat_bot:wechatbot"
]

setup(
    name="wechatbot",
    version='1.0.2',
    description="a wechat bot developed for geeks",
    long_description="",
    author="chuanwu",
    author_email="chuanwusun@gmail.com",
    packages=['wechatbot'],
    url="https://github.com/chuanwu/WechatBot.py",
    entry_points={"console_scripts": entry_points},
    install_requires=[],

)
