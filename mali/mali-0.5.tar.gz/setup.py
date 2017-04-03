# coding=utf-8
import os
from setuptools import setup

build = 0


def __path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

if os.path.exists(__path('pip_build.info')):
    build = open(__path('pip_build.info')).read().strip()

keywords = ''
if os.path.exists(__path('pip_build.keywords.info')):
    keywords = open(__path('pip_build.keywords.info')).read().strip()

version = '0.{}'.format(build)

setup(
    name='mali',
    version=version,
    py_modules=['mali'],
    install_requires=[
        'click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        mali=mali:cli
    ''',
)
