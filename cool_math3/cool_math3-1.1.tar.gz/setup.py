from distutils.core import setup
from setuptools import find_packages

setup(
    name="cool_math3",
    packages=find_packages(exclude=["*.test", "*.test.*", "test"]),
    version='1.1',
    description='Cool math',
    author='missingdays',
    author_email='rebovykin@gmail.com',
    url='https://github.com/missingdays/cool_math3',
    download_url='https://github.com/missingdays/cool_math3/archive/1.1.tar.gz',
    keywords=['math'],
    scripts=['bin/cool_math3'],
    install_requires=['scipy']
)
