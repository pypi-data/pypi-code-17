# -*- coding:utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import lawes

VERSION = [str(version) for version in lawes.VERSION if version != 'alpha']
VERSION = '.'.join(VERSION)

setup(
    name='Lawes',
    description='',
    long_description='',
    classifiers=[],
    keywords='',
    author='Lawes',
    author_email='haiou_chen@sina.cn',
    url='https://github.com/MrLawes/Lawes',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'pymongo>=2.8',
    ],
    version=VERSION,
)
