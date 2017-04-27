# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))


entry_points = [
]

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name="fastrpc",
    version='0.0.1',
    description="Convert postman collections to function calls.",
    long_description=long_description,
    author="chuanwu",
    author_email="chuanwusun@gmail.com",
    packages=["fastrpc"],
    url="https://github.com/chuanwu/fastrpc.py",
    entry_points={"console_scripts": entry_points},
    install_requires=[
        "click==6.7"
    ],
)
