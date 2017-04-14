#!/usr/bin/env python3
from distutils.core import setup

version = "0.0.2"

setup(
    name = 'awhois',
    packages = ['awhois'], # this must be the same as the name above
    license = 'MIT',
    version = version,
    description = 'Whois like command to describe an AWS service by hostname or service.',
    author = 'Manoel Carvalho',
    author_email = 'manoelhc@gmail.com',
    url = 'https://github.com/manoelhc/awhois', # use the URL to the github repo
    download_url = 'https://github.com/manoelhc/awhois', # I'll explain this in a second
    keywords = ['testing', 'network'], # arbitrary keywords
    install_requires=[
        'boto3',
        'awscli'
    ],
    classifiers = [
        'Topic :: Internet',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    entry_points={
        'console_scripts': [
            'awhois=awhois:main',
        ],
    }
)
