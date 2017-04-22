#!/usr/bin/env python
# encoding: utf-8


"""
@version : 
@author  : 
@license : 
@contact : jxm_zn@163.com
@site    : http://blog.csdn.net/jxm_csdn
@software: PyCharm
@time    : 17-2-13 下午5:14
"""
from setuptools import setup

setup(
    name='loginit',       # 应用名
    version='1.2.1',        # 版本号
    description='The logging init model',
    url="https://git.oschina.net/myPyLib/log-Init",
    author = 'Jiangxumin',
    author_email = 'jxm_zn@163.com',
    license='MIT',
    packages=['loginit'], # 包括在安装包内的Python包
    include_package_data=True, # 启用清单文件MANIFEST.in
    zip_safe = False,          #不压缩为一个egg文件，而是以目录的形式安装egg

)


