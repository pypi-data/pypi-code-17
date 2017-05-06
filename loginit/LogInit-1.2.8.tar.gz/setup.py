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
from setuptools import setup, find_packages

long_description = ""
try:
    long_description = file('README.rst').read()
except Exception:
    pass


setup(
    name='LogInit',         # 应用名
    version='1.2.8',        # 版本号
    description='The logging init model',
    long_description=long_description,
    url="https://git.oschina.net/myPyLib/log-Init",
    packages=find_packages(),
    #packages=['loginit'],  # 包括在安装包内的Python包
    author = 'Jiangxumin',
    author_email = 'jxm_zn@163.com',
    license='MIT',
    platforms=['any'],
    include_package_data=True, # 启用清单文件MANIFEST.in
    zip_safe = False,          #不压缩为一个egg文件，而是以目录的形式安装egg

)


