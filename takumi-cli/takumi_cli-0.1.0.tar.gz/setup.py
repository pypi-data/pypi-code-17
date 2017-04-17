#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='takumi_cli',
    version='0.1.0',
    description='Takumi service framework command line toolkit',
    long_description=open("README.rst").read(),
    author="Eleme Lab",
    author_email="imaralla@icloud.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/elemecreativelab/takumi-cli',
    install_requires=[
        'takumi',
        'takumi-ext',
        'takumi-config',
        'docopt',
        'schema',
        'gevent>=1.2.1',
        'thriftpy',
        'gunicorn',
    ],
    extras_require={
        'deploy': ['ansible>=2.2.0.0'],
        'shell': ['takumi-client', 'IPython']
    },
    entry_points={
        'console_scripts': [
            'takumi = takumi_cli.cmds:main'
        ]
    }
)
