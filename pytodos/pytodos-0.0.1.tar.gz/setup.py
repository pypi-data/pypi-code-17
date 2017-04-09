# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

entry_points = [
    # todo
    "todos = PyTodos.todo:todos"
]

with open("README.md") as f:
    long_description = f.read()


setup(
    name="pytodos",
    version='0.0.1',
    description="",
    long_description=long_description,
    author="chuanwu",
    author_email="chuanwusun@gmail.com",
    packages=find_packages(),
    url="https://github.com/chuanwu/PyToDos.py",
    entry_points={"console_scripts": entry_points},
    install_requires=[],

)
