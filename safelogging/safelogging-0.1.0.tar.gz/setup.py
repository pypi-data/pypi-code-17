from os import path
from codecs import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='safelogging',

    version='0.1.0',

    description='Extensions to the standard python logging framework',
    long_description=long_description,

    url='https://github.com/Procera/python-safelogging',

    author='Pontus Andersson',
    author_email='pontus.andersson@proceranetworks.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords='python safe logging syslog',

    packages=find_packages(),
)
