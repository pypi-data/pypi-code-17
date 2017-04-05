#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='cryoproxy',
    version='2017.4.5',
    packages=[''],
    url='https://hg.3lp.cx/cryoproxy',
    license='GPL',
    author='Vadim Dyadkin',
    author_email='diadkin@esrf.fr',
    description='Asynchronous serial port proxy daemon for Cryostream based on asyncio',
    requires=[
        'pyserial',
    ],
    entry_points={
        'console_scripts': [
            'cryoproxy=cryoproxy:main',
        ],
    },
)
