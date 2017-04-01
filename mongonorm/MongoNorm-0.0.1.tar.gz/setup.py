from setuptools import setup

VERSION = '0.0.1'

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='MongoNorm',
    version='0.0.1',
    description="MongoNorm is Not a Object Relational Mapping library "
                "for mongodb.",
    long_description=long_desc,
    url='https://github.com/CrowsT/MongoNorm',
    author='Crows',
    author_email='pt.wenhan@gmail.com',
    packages=['mongonorm'],
    install_requires=[
        'PyMongo(>=3.0)'
    ],
    license='BSD 2-Clause License'
)
