import os
from setuptools import setup

setup(
        name='hdv_sqlalchemywrapper',
        packages=["hdv_sqlalchemywrapper"],
        version='0.0.5',
        author='Alex Hyojun Kim',
        author_email='alex@hotdev.com',
        description='',
        license='BSD',
        install_requires=[
            'sqlalchemy', 
            'pymysql'],
      )