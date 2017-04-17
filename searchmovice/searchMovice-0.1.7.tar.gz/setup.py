#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='searchMovice',
    version='0.1.7',
    author='passer',
    author_email='904727147@qq.com',
    url='https://zhuanlan.zhihu.com/passer',
    description=u'输入关键词搜索百度网盘中的电影资源',
    packages=['searchMovice'],
    install_requires=['bs4','requests'],
    entry_points={
        'console_scripts': [
            'smv=searchMovice:main'
        ]
    }
)
