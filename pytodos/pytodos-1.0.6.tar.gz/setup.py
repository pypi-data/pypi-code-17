# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

entry_points = [
    "add=PyTodos.todo:add",
    "list=PyTodos.todo:list",
    "got=PyTodos.todo:kill"
]

setup(
    name="pytodos",
    version='1.0.6',
    description="",
    long_description="",
    author="chuanwu",
    author_email="chuanwusun@gmail.com",
    packages=find_packages(),
    url="https://github.com/chuanwu/PyToDos.py",
    entry_points={"console_scripts": entry_points},
    install_requires=[],
)
