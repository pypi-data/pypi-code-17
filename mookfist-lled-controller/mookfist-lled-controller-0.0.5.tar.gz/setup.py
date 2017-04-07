import os
from setuptools import setup

__doc__ = """Mookfist LimitlessLED Controller

A python library for communicating with LimitlessLED compatible wifi bridges.

Bridge Version Support:

    v4 - Compatible
    v5 - Compatible
    v6 - Not Compatible
"""

desc = open('README.md').read()



setup(
    name="mookfist-lled-controller",
    description=__doc__,
    version="0.0.5",
    author="mookfist",
    author_email="mookfist@gmail.com",
    url="https://github.com/mookfist/mookfist-lled-controller",
    scripts=['lled.py'],
    packages=['mookfist_lled_controller'],
    install_requires=[
        'docopt',
        'colorama'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    keywords=['milight','limitlessled']
)
