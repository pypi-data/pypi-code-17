#!/usr/bin/env python3.6
# coding: utf-8

from setuptools import setup, find_packages


setup(
    name='intersectshape',
    version='0.1.1',
    packages=find_packages(),
    author='Jonathan Virga',
    author_email='jonathan.virga@gmail.com',
    description='Reverse geocoding from a shapefile of polygons.',
    long_description=open('README.rst').read(),
    install_requires=["numpy", "shapely", "pyshp"],
    include_package_data=True,
    url="https://github.com/jnth/intersectshape",
    license="GNU GPL v3"
)
