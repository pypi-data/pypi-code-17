#!/usr/bin/env python

from setuptools import setup

setup(name='pdf-counter',
      version='0.1.1',
      description='Sum up the pages of all pdf files in a folder',
      url='http://github.com/pvskand/pdf-page-counter',
      author='Skand',
      author_email='pvskand@gmail.com',
      license='MIT',
      scripts=['bin/pdf-page-counter'],
      packages=['pdf-page-counter'],
      install_requires=[
          'argparse',
          'terminaltables',
          'PyPDF2'
      ],
      zip_safe=False)

