#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='MTObjectFirstInPython',
    version='0.0.2',
    description="Application of Object First approach for Python using Pygame",
    long_description=readme + '\n\n' + history,
    author="Pavol Megela",
    author_email='pavol.megela@gmail.com',
    url='https://github.com/PaulliDev/MTObjectFirstInPython',
    packages=[
        'MTObjectFirstInPython',
    ],
    package_dir={'MTObjectFirstInPython':
                 'MTObjectFirstInPython'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='MTObjectFirstInPython',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
