#!/usr/bin/python3
# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name='pyclt',
    version='0.7.2',
    author='zsh2401',
    author_email='zsh2401@163.com',
    url='https://github.com/zsh2401/PYCLT',
    description='一个快捷的命令行翻译软件!按照GPL-3.0协议开源!',
    packages=['pyclt','pyclt.res','pyclt.interface','pyclt.api'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cltb=pyclt:run4baiduApi',
            'cltj=pyclt:run4jinshanApi',
            'cltn=pyclt:run4neteaseApi',
            'clts=pyclt:run4neteaseSpider',
            'pyclt=pyclt:run4pyclt',
        ]
    }
)
