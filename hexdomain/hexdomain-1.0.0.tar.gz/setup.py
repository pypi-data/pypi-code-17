# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='hexdomain',
    version='1.0.0',
    url='https://github.com/benwebber/hexdomain/',

    description='Generate domain names that only contain hexadecimal numbers.',
    long_description=open('README.rst').read(),

    author='Ben Webber',
    author_email='benjamin.webber@gmail.com',

    py_modules=['hexdomain'],
    install_requires=[
        'tld',
        'six',
    ],

    zip_safe=False,

    entry_points={
        'console_scripts': [
            'hexdomain = hexdomain:main',
        ],
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
