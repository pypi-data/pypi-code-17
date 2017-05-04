#!/usr/bin/env python

from setuptools import setup
import chuk

setup(
    name="chuk",
    version=chuk.version,
    author="Chris Markiewicz, Bram Cohen, John Hoffman, Uoti Arpala et. al.",
    author_email="<effigies@gmail.com>",
    description="John Hoffman's fork of the original bittorrent",
    license="MIT",
    install_requires=['win_inet_pton'],
    packages=["chuk",
              "chuk.Application",
              "chuk.Client",
              "chuk.Meta",
              "chuk.Network",
              "chuk.Storage",
              "chuk.Tracker",
              "chuk.Download"]
)
