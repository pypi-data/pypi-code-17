"""For distribution.
"""

from setuptools import setup, find_packages

# build with sdist to make sure platform compatibility.
# Theano packages are not included.
setup(
    name="deepmodels",
    version="0.2.3",
    description="framework for build, train and test deep learning models",
    url="https://github.com/flyfj/deepmodels",
    author="Jie Feng",
    author_email="jiefengdev@gmail.com",
    license="MIT",
    include_package_data=True,
    packages=find_packages(exclude=["docs"]),
    install_requires=[])
