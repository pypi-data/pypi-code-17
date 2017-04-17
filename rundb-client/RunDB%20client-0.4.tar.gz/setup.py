# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='RunDB client',
    version='0.4',
    packages=find_packages(),
    # namespace_packages=['rundb'],
    url='https://git.kern.phys.au.dk/ausa/RunDBC',
    license='MIT',
    author='Michael Munch & Jesper Halkjær',
    author_email='mm@phys.au.dk',
    description='Client API for RunDB',
    install_requires=[
        'requests>2',
    ]
)
