import os
from setuptools import setup

setup(
        name = 'hdv_scalr',
        packages = ["hdv_scalr"],
        version = '0.1.0',
        author = 'Alex Hyojun Kim',
        author_email = 'alex@hotdev.com',
        description = ' ',
        license = 'BSD',
        install_requires = ['requests', 'xmltodict'],
        entry_points = {
                  'console_scripts': [
                                     'hdvscalr = hdvscalr.__main__:main'
                                     ]
                  }
      )