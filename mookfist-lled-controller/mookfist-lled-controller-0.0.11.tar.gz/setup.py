import os
from setuptools import setup

__doc__ = """A python library for communicating with LimitlessLED/Milight/Easybulb compatible wifi bridges."""

setup(
    name="mookfist-lled-controller",
    description=__doc__,
    version="0.0.11",
    author="mookfist",
    author_email="mookfist@gmail.com",
    url="https://github.com/mookfist/mookfist-lled-controller",
    scripts=['lled.py'],
    packages=['mookfist_lled_controller','mookfist_lled_controller.bridges'],
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
