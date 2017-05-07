#!/usr/bin/env python

from setuptools import setup

with open("README.rst") as readme:
    long_description = readme.read()

install_requires = []

setup(
    name='cdmc',
    version='0.1.1',
    description='Tools for using the Cinco De Mayo Calendar',
    long_description=long_description,
    author='Robert Miles',
    author_email='milesrobert374@gmail.com',
    url='https://github.com/MineRobber9000/cdmc',
    keywords='novelty-calendars',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['cdmc'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'cdmdate=cdmc.console:cdmdate',
            'cdmdateconv=cdmc.console:cdmdateconv',
        ],
    }
)
