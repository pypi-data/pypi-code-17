# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""


import re
from setuptools import setup
import os


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('trail/trail.py').read(),
    re.M
).group(1)
print("Got version: {}".format(version))

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

config_dir = "{}/.trail".format(os.path.expanduser("~"))  # is the home dir; "global" trails are kept here.
print("config dir is: {}".format(config_dir))

setup(
    name='trail',
    packages=['trail'],  # this must be the same as the name above
    entry_points={
        "console_scripts": ['trail = trail.trail:main']
    },
    data_files=[
        (config_dir, [])
    ],
    version=version,
    description='Keep track of your thoughts.',
    long_description=long_descr,
    author='tolbot',
    author_email='eltolis@hotmail.com',
    url='https://github.com/tolbot/trail',  # use the URL to the github repo
    download_url='https://github.com/tolbot/trail/archive/{}.tar.gz'.format(version),  # make sure proper github tags are added; see below
    keywords=['todo', 'productivity', 'notes'],  # arbitrary keywords
    classifiers=[],
)
