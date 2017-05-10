#!/usr/bin/env python
from setuptools import setup
import ast
import re

_version_re = re.compile(r'__version__=(.*)') 

with open('kli/__init__.py', 'r') as f:
    version = str(ast.literal_eval(_version_re.search(f.read()).group(1)))

setup(
    name='kli',
    version=version,
    description='',
    author='Shriram Sunder',
    author_email='shriram.sunder121091@gmail.com',
    url='',
#    packages=['kli'],
    py_modules=['kli.main','kli.classes', 'kli.imports', 'kli.support'],
    entry_points={'console_scripts': ['kli=kli.main:kli']},
    install_requires=['cryptography' , 'argcomplete', 'click', 'bs4', 'tqdm', 'requests', 'appdirs'],
    )
