import os
from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="djangomultitenant",
    version="0.0.2",
    author="Akhil Lawrence",
    author_email="akhilputhiry@gmail.com",
    description=("A django app which helps to implement multitenancy easily"),
    license="GNU GPLv3",
    keywords="multitenant, multitenancy, django multitenant, django multitenancy",
    url="https://github.com/akhilputhiry/djangomultitenant",
    packages=["djangomultitenant"],
    install_requires=[str(i.req) for i in parse_requirements("./requirements.txt", session=PipSession())],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "License :: Freeware",
    ],
)