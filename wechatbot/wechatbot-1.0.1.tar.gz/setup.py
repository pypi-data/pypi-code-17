# -*- coding: utf-8 -*-

from setuptools import setup

entry_points = [
    # todo
    "wechatbot = WechatBot.wechat_bot:wechatbot"
]

setup(
    name="wechatbot",
    version='1.0.1',
    description="",
    long_description="",
    author="chuanwu",
    author_email="chuanwusun@gmail.com",
    packages=['wechatbot'],
    url="https://github.com/chuanwu/WechatBot.py",
    entry_points={"console_scripts": entry_points},
    install_requires=[],

)
