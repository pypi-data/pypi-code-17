import os
import sys

if sys.version_info[0:2] < (3, 5):
    raise Exception("aiopixiv requires Python 3.5+")

from setuptools import setup

rootpath = os.path.abspath(os.path.dirname(__file__))


def extract_version(module='aiopixiv'):
    version = None
    fname = os.path.join(rootpath, module, '__init__.py')
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                _, version = line.split('=')
                version = version.strip()[1:-1]  # Remove quotation characters.
                break
    return version


setup(
    name='aiopixiv',
    version=extract_version(),
    packages=['aiopixiv'],
    url='https://github.com/SunDwarf/aiopixiv',
    license='MIT',
    author='Isaac Dickinson',
    author_email='sun@veriny.tf',
    description='An asyncio wrapper for the Pixiv API.',
    install_requires=[
        "aiohttp>=2.0.0,<=2.0.4"
    ]
)
