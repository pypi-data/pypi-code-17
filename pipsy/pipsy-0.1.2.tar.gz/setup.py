# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pipsy',
    version="0.1.2",
    description='Shows updates for installed packages',
    long_description='Shows available updates and security notices for installed packages',
    author='Donovan Schönknecht',
    author_email='don@tpyo.net',
    url='https://github.com/tpyo/pipsy',
    packages=['pipsy'],
    license='MIT',
    include_package_data=True,
    install_requires=[
        'pip>=9.0.1',
        'changelogs>=0.9.0',
        'packaging>=16.8',
    ],
    entry_points={
        "console_scripts": [
            "pipsy=pipsy:main",
        ],
    },
    extras_require={
        'testing': ['pytest', 'mock'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
)
