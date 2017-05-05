import os
from setuptools import setup

setup(
        name = 'hdv_pyrun',
        packages = ["hdv_pyrun"],
        version = '0.1.1',
        author = 'Alex Hyojun Kim',
        author_email = 'alex@hotdev.com',
        description = ' ',
        license = 'BSD',
        install_requires = [
                            'paramiko', 
                            'invoke',
                            'hdv_dummy',
                            'hdv_logging'
                            ],
        entry_points = {}
      )