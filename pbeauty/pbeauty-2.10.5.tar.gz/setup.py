#!/usr/bin/env python
import os
import sys

from redis import __version__

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            # import here, because outside the eggs aren't loaded
            import pytest
            errno = pytest.main(self.test_args)
            sys.exit(errno)

except ImportError:

    from distutils.core import setup

    def PyTest(x):
        x


setup(
    name='pbeauty',
    version=__version__,
    description='protobuf parse and beauty tools',
    long_description='protobuf parse and beauty tools',
    url='http://github.com/',
    author='Linggui Wang',
    author_email='pthread_t@qq.com',
    maintainer='Linggui Wang',
    maintainer_email='pthread_t@qq.com',
    keywords=['protobuf', 'format' 'beauty'],
    license='MIT',
    packages=['pbeauty'],
    tests_require=['pytest>=2.5.0'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
