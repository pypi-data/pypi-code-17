
from distutils.core import setup
from setuptools import find_packages

setup(
    name='cool_math2',
    packages=find_packages(exclude=['test', '*.test', '*.test.*']),
    version='1.1.5',
    description='Cool math',
    author='missingdays',
    author_email='rebovykin@gmail.com',
    url='https://github.com/missingdays/cool_math2',
    download_url='https://github.com/missingdays/cool_math2/archive/1.1.5.tar.gz',
    keywords=['math'],
    scripts=['bin/cool_math2'],
    install_requires=['scipy']
)
