import os
from setuptools import setup, Extension
from glob import glob

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
    'boto3',
    ]

setup(
    name = "net-tools",
    version = "0.0.2",
    author = "Choonho Son",
    author_email = "choonho.son@gmail.com",
    description = ("Network measurement tool set for cloud provisioning"),
    license = "Apache",
    keywords = "cloud network measurement latency discovery",
    url = "https://github.com/choonho/net-tools",
    packages=['nettools','nettools.provider', 'nettools.sensor', 'nettools.utils'],
    long_description=read('nettools/README.md'),
    classifiers=[
        "Topic :: Utilities"
    ],
    zip_safe=True,
    install_requires= requirements,
    entry_points = {
        'console_scripts': [
            'net-tools = nettools.cli:main',
            ],
        },
)
