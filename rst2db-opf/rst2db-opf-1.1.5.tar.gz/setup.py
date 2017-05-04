#!/usr/bin/env python
from setuptools import setup, find_packages

long_desc = """
Usage
-----

::

 rst2db-opf <filename> [-e root_element] [-o output_file] [-t template_file]

Only the filename to process is required. All other settings are optional.

Settings:

  -e root_element  set the root element of the resulting docbook file. If this
                   is not specified, then 'section' will be used.

  -o output_file  set the output filename to write. If this is not specified,
                  then output will be sent to stdout.

  -t template_file  set a template file to use to dress the output. You must
                    have Jinja2 installed to use this feature.

                    Use {{data.root_element}} and {{data.contents}} to
                    represent the output of this script in your template.
"""

setup(name='rst2db-opf',
      description="""
        A reStructuredText to Docbook converter using Python's docutils.""",
      version='1.1.5',
      install_requires=['docutils>=0.12', 'lxml>=2.3'],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'rst2db-opf = openpowerfoundation.cmd_rst2db_opf:run'
              ],
          },
      author='OpenPOWER System Software Work Group Chair',
      author_email='syssw-chair@openpowerfoundation.org',
      url='https://github.com/OpenPOWERFoundation/rst2db-opf',
      )
