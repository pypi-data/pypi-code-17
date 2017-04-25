#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='uninstall_app',
    version='0.0.1',
    author='allen',
    author_email='437806668@qq.com',
    url='https://allenwu.itscoder.com',
    description=u'自动化卸载app',
    packages=['uninstall_app'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cl=uninstall_app:clear1',
            'ca=uninstall_app:clear2',
            'cc=uninstall_app:clear3'
        ]
    }
)