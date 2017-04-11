from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

setup (
    name='zerotier',
    version='1.0.1',
    description='Zerotier API client',
    url='https://github.com/g8os/zerotier_client',
    author='Christophe de Carvalho',
    author_email='christophe@gig.tech',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.13.0',
        'python-dateutil>=2.6.0',
    ],
)
