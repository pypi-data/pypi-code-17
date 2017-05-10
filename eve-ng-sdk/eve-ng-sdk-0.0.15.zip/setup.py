from os import path
from setuptools import setup, find_packages


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='eve-ng-sdk',
    description='EVE-NG REST API Library',
    author='Sean Larimore',
    long_description=read('README'),
    version='0.0.15',
    packages=find_packages(exclude=['tests']),
    keywords='eve-ng unetlab rest api sdk library client',
    license='MIT',
    url='https://github.com/slarimore02/eve-ng-python-sdk.git',
    install_requires=['requests'],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Programming Language :: Python :: 2.7',
    ],
)
