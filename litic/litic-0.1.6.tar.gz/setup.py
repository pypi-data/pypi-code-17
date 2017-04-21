# Always prefer setuptools over distutils
# from setuptools import setup, find_packages
from distutils.core import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='litic',
    version='0.1.6',
    description='A LITIC Service is a set of procedures that can be called from an external program using HTTP.',
    long_description='A LITIC Service is a set of procedures that can be called from an external program using HTTP.  We provide SDKs for Python to simplify calling the service.',
    url='https://litic.com',
    # download_url='',
    author='LITIC Team',
    author_email='development@litic.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['LITIC'],
    packages=[
        'litic',
        'litic.exceptions'
    ],
    install_requires=[
        'requests',
        'pandas',
        'six'
    ]
)
