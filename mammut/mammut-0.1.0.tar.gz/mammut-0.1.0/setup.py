# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

tests_require = ['pytest',]

setup(
    name='mammut',
    version='0.1.0',
    description='',
    long_description='',
    license="MIT",
    author="kk6",
    author_email="hiro.ashiya@gmail.com",
    url="https://github.com/kk6/mammut",
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'requests-oauthlib>=0.8.0',
        'requests>=2.13.0',
    ],
    setup_requires=['pytest-runner', ],
    tests_require=tests_require,
    extras_require={'testing': tests_require},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"
    ],
)

