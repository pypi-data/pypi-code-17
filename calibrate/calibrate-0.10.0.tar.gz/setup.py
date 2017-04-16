#!/usr/bin/env python

from setuptools import setup

setup(
  name='calibrate',
  version='0.10.0',

  author='Ginkgo Bioworks, Benjie Chen',
  author_email='devs@ginkgobioworks.com, benjie@alum.mit.edu',

  description='Interpolate using a calibration curve',
  long_description=open('README.rst').read(),
  url='https://github.com/ginkgobioworks/calibrate',

  license='MIT',
  keywords='calibrate calibration linear regression power regression fit quantify',
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Artificial Life',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Scientific/Engineering :: Chemistry',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],

  py_modules=['calibrate'],
  include_package_data=True,
  zip_safe=True,
  install_requires=[
    'numpy',
    'scipy',
    'six',
  ],
  tests_require=[
    'nose',
    'coverage',
  ],
)
