"""
setup.py
~~~~~~~~

Publishing related configurations
"""
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = 'deliverybot-utils'
DESCRIPTION = 'A handful set of functionalities shared across all services, written in Python'
AUTHOR = 'Gabriel Lima'
AUTHOR_EMAIL = 'gvclima@gmail.com'
URL = 'https://github.com/deliverybot/utils'
VERSION = '0.15.0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='MIT',
    url=URL,
    packages=['deliverybot_libs'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[]
)
