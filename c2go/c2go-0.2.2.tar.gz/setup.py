import os
import versioneer

from setuptools import setup, find_packages
from contextlib import suppress
from setuptools.dist import Distribution

with suppress(Exception):
    Distribution({'setup_requires': ['setuptools-markdown']})

setup(
    name='c2go',
    version=versioneer.get_version(),
    description='c to go conversion',
    author='Mars Galactic',
    author_email='xoviat@users.noreply.github.com',
    url='https://github.com/xoviat/c2go',
    packages=find_packages(),
    license=open(
        os.path.join(os.path.dirname(__file__), 'LICENSE')).readline().strip(),
    platforms='any',
    classifiers=[],
    entry_points={
        'console_scripts': ['c2go = c2go.__main__:main'],
    },
    install_requires=['pycparser'],
    cmdclass=versioneer.get_cmdclass(),
    long_description_markdown_filename='README.md')
