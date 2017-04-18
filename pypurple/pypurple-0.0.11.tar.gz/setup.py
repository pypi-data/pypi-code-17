#!/usr/bin/python3

import sys

from setuptools import setup, Extension
from subprocess import Popen, PIPE

EXT_PKG_CONFIG_TOOL='pkg-config'
PKG_CONFIG_PACKAGE='purple'

if '--use-cython' in sys.argv:
    USE_CYTHON = True
    sys.argv.remove('--use-cython')
else:
    USE_CYTHON = False

def get_cflags():
    return Popen([EXT_PKG_CONFIG_TOOL, '--cflags', PKG_CONFIG_PACKAGE], stdout=PIPE).communicate()[0].decode().split()

def get_ldflags():
    return Popen([EXT_PKG_CONFIG_TOOL, '--libs', PKG_CONFIG_PACKAGE], stdout=PIPE).communicate()[0].decode().split()

long_description = "\
Python bindings for libpurple, a multi-protocol instant messaging library."

sourcefiles = ['pypurple/pypurple.pyx', 'pypurple/c_purple.c']
extensions = [Extension("pypurple", sourcefiles,
                        extra_compile_args=get_cflags(),
                        extra_link_args=get_ldflags())]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions, include_path=["pypurple/libpurple"])

setup(
    name='pypurple',
    version='0.0.11',
    author='Andrey Petrov',
    author_email='andrey.petrov@gmail.com',
    packages=['pypurple'],
    description='Python bindings for Purple',
    url="https://github.com/anpetrov/python-purple",
    download_url="https://github.com/anpetrov/python-purple/archive/0.0.1.tar.gz",
    long_description=long_description,
    include_package_data=True,
    ext_modules=extensions
)
