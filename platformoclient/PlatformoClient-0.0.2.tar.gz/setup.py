# -*- coding: utf-8 -*-


from setuptools import setup

__author__ = 'zhengz'

setup(
    name='PlatformoClient',
    version='0.0.2',
    description=u'收集Flask的请求响应时间并发送至logstash',
    keywords='logstash flask',

    license='MIT',
    install_requires=['requests'],

    author='zhengz',
    author_email='zhengz@miriding.com',

    packages=['PlatformoClient']
)
