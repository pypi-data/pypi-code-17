from __future__ import print_function  
from setuptools import setup, find_packages  
import sys  
  
setup(  
    name="sistdmyy",
    version="1.2.3",
    author="lanmengfei",
    author_email="865377886@qq.com",
    description="兰孟飞在深圳标准技术研究部的工作",
    long_description=open("README.txt",encoding="utf-8").read(),
    license="MIT",
    url="https://user.qzone.qq.com/865377886",
    packages=['sistdmyy','sistdmyy.dz'],
    install_requires=[
        "pandas",
        "sqlalchemy",
        "pymssql",
        "jieba",
        "numpy"
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