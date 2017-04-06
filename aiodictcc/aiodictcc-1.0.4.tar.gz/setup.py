import os
import sys

if sys.version_info[0:2] < (3, 5):
    raise Exception("aiodictcc requires Python 3.5+")

from setuptools import setup

rootpath = os.path.abspath(os.path.dirname(__file__))


def extract_version(_module='aiodictcc'):
    version = None
    fname = os.path.join(rootpath, _module, '__init__.py')
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                _, version = line.split('=')
                version = version.strip()[1:-1]
                break
    return version


setup(
    name='aiodictcc',
    version=extract_version(),
    packages=['aiodictcc'],
    url='https://github.com/ilevn/aiodictcc',
    license='MIT',
    author='Nils Theres',
    author_email='nilsntth@gmail.com',
    description='An asyncio-based wrapper for dict.cc',
    install_requires=['aiohttp>=2.0.5', 'lxml==3.7.3']
)
