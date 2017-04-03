# The MIT License (MIT)
#
# Copyright (c) 2017 Doublify Technologies
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
from setuptools import find_packages, setup

DEPENDENCIES = ('protobuf>=3.2.0', )

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='doublify-toolkit',
    version='0.4.1',
    author='Doublify APIs',
    author_email='opensource@doublify.io',
    description='Doublify API toolkit for Python',
    long_description=long_description,
    url='https://github.com/doublifyapis/toolkit-python',
    packages=find_packages(),
    namespace_packages=('doublify', ),
    install_requires=DEPENDENCIES,
    license='MIT',
    keywords='doublify toolkit',
    classifiers=('Development Status :: 2 - Pre-Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Topic :: Internet :: WWW/HTTP',
                 'Topic :: Software Development',
                 'Topic :: Text Processing :: Filters', ), )
