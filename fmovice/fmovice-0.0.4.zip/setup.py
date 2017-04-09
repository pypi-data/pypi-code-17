#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='fmovice',
    version='0.0.4',
    author='passer',
    author_email='904727147@qq.com',
    url='https://zhuanlan.zhihu.com/passer',
    description=u'输入关键词搜索两大百度网盘提供商中的电影资源',
    packages=['fmovice'],
    install_requires=['bs4','requests'],
    entry_points={
        'console_scripts': [
            'fmv=fmovice:main'
        ]
    }
)