import os
from setuptools import setup

desc = open('README.md').read()

setup(
    name="mookfist-lled-controller",
    description=desc,
    version="0.0.4",
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
