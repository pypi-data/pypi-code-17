#!/usr/bin/python3 
# coding=utf-8

from setuptools import setup

setup(name='hiwi',
      version='0.1',
      description='Integrate or share otree experiments with ease',
      url='http://github.com/chkgk/hiwi',
      author='Christian König genannt Kersting',
      author_email='christian.koenig@awi.uni-heidelberg.de',
      license='MIT',
      packages=['hiwi'],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['node'],
      entry_points={
        'console_scripts': [
          'hiwi = hiwi.main:main',
        ]
      },
      install_requires=[
        'docopt',
      ]
    )