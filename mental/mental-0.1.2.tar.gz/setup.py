import os
import re

from setuptools import setup, find_packages


def read_version(version_file_name):
    """
    Reads the package version from the supplied file
    """
    version_file = open(os.path.join(version_file_name)).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", version_file).group(1)

name = 'mental'
version = read_version(os.path.join(name,'__init__.py'))

setup(
    name=name,
    version=version,
    description='Mental poker implementation',
    url='https://github.com/colonelmo/mental-poker',
    download_url='https://github.com/colonelmo/mental/archive/0.1.0.tar.gz',
    author='Mohammad Nasirifar',
    author_email='far.nasiri.m@gmail.com',
    license='BSD',
    keywords='mental poker rsa cryptography',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=True,
    install_requires = [],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
)
