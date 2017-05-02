from __future__ import print_function  
from setuptools import setup, find_packages  
import sys  
  
setup(  
    name="lmfxx",
    version="1.0.0",
    author="lanmengfei",
    author_email="865377886@qq.com",
    description="兰孟飞在深圳标准技术研究部的工作",
    long_description=open("README.rst").read(),
    license='LICENSE.txt',
    url="https://github.com/lanmengfei/testdm",
    packages=['lmfxx'],
    install_requires=[
        "pandas >= 0.13",

        ],  
    classifiers=[  
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ],  
)  