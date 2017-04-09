from setuptools import setup
from setuptools import find_packages

import jobcan

with open('README.rst', "r") as f:
    long_description = f.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name=jobcan.__name__,
    packages=find_packages(),
    version=jobcan.__version__,
    author=jobcan.__author__,
    author_email=jobcan.__email__,
    description="Command for jobcan automation",
    long_description=long_description,
    url=jobcan.__url__,
    license=jobcan.__license__,
    install_requires=[
        'click>=2.0',
        'html5lib>=0.999999999',
        'mechanize>=0.3.1',
        'requests>=2.13.0',
        'typing'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Environment :: Console"
    ],
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      jobcan = jobcan.jobcan:main
    """,
)
