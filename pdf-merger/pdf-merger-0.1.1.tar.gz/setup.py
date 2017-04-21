#!/usr/bin/env python

from setuptools import setup

setup(name='pdf-merger',
      version='0.1.1',
      description='Merges PDFs',
      url='http://github.com/pvskand/pdf-merger',
      author='Skand Vishwanath Peri',
      author_email='pvskand@gmail.com',
      license='MIT',
      scripts=['bin/pdf-merger'],
      packages=['pdf-merger'],
      install_requires=[
          'argparse',
          'PyPDF2'
      ],
      zip_safe=False)

