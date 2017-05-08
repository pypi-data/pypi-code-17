#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'dnaseq_validation',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.4,
      description = 'validate dnaseq workflow based on fastqc, picard and samtools metrics',
      url = 'https://github.com/NCI-GDC/dnaseq_validation',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': ['dnaseq_validation=dnaseq_validation.__main__:main']
          },
)
