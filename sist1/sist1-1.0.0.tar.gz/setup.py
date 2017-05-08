from __future__ import print_function  
from setuptools import setup, find_packages  
import sys  
  
setup(  
    name="sist1",
    version="1.0.0",
    author="lannan",
    author_email="865377886@qq.com",
    description="兰楠在深圳标准技术研究部的工作",
    long_description=open("README.txt",encoding="utf-8").read(),
    license="nan",
    url="https://user.qzone.qq.com/865377886",
    packages=['sist1'],
    install_requires=[
        "pandas"
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
    ]
)