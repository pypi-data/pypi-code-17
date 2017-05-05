import os
from setuptools import setup, find_packages


setup(
        name='hdv_emails',
        packages=["hdv_emails"],
        version='0.0.1',
        author='Alex Hyojun Kim',
        author_email='alex@hotdev.com',
        description='Simple wrapper class for emails',
        url='https://github.com/jk43/hdv_emails',
        download_url='https://github.com/jk43/hdv_emails.git',
        license='BSD',
        install_requires=[
            'emails==0.5.13',
            ],
        entry_points={},
      )