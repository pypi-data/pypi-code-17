#!/usr/bin/env python
import io
from setuptools import setup


def read(fname):
    with io.open(fname, encoding='utf8') as fp:
        content = fp.read()
    return content

setup(
    name="judyz-cffi",
    version="0.8.3a1",
    long_description=read("README.rst"),
    packages=["judyz_cffi"],
    # package_data={
    #     "judyz-cffi": [
    #         "judy_cffi/_build.py",
    #         "judy_cffi/Judy_cffi.h",
    #         "LICENSE",
    #         "README.rst",
    #         # "judy_cffi/_judy_cffi.py",
    #     ],
    # },
    # py_modules=["judyz_cffi"],
    author="Yves Bastide",
    author_email="yves@botify.com",
    description="Python CFFI Judy wrapper",
    url="https://github.com/botify-labs/judyz",
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["judyz_cffi/_build.py:ffi"],
    install_requires=["cffi>=1.0.0"],
    test_suite="tests",
    tests_require=[
        'nose',
    ],
    license=read("LICENSE"),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
