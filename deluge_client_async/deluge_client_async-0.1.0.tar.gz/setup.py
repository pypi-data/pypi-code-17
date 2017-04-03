#!/usr/bin/env python

from __future__ import with_statement

from setuptools import setup

with open("README") as readme:
    documentation = readme.read()

setup(
    name="deluge_client_async",
    version="0.1.0",

    description="An asyncio client to deluge.",
    long_description=documentation,
    author="AllSeeingEyeTolledEweSew",
    author_email="allseeingeyetolledewesew@protonmail.com",
    license="Unlicense",
    py_modules=["deluge_client_async"],
    url="http://github.com/allseeingeyetolledewesew/deluge_client_async",
    python_requires=">=3.4",
    install_requires=[
        "rencode>=1.0.0",
        "pyxdg>=0.25",
    ]
)
