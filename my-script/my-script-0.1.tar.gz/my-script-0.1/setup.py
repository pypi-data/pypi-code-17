#!/usr/bin/python
#from setuptools import setup
from distutils.core import setup 
setup(
     name='my-script',    # This is the name of your PyPI-package.
     version='0.1',                          # Update the version number for new releases
     scripts=['my_script']                  # The name of your scipt, and also the command you'll be using for calling it
 )
