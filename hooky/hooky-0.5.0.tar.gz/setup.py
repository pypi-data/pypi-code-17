from setuptools import setup

import hooky

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

NAME = 'hooky'

DESCRIPTION = 'A module contain list-like and a dict-like classes with hook point.'

URL = 'https://github.com/meng89/' + NAME

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(name=NAME,
      version=hooky.__version__,
      description=DESCRIPTION,
      author='Chen Meng',
      author_email='ObserverChan@gmail.com',
      license='MIT',
      url=URL,
      classifiers=CLASSIFIERS,
      py_modules=['hooky'],
      tests_require=['nose'],
      test_suite='nose.collector',
      )
