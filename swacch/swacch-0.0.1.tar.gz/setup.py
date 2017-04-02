from setuptools import setup, find_packages
import sys,os

setup(name='swacch',
     version='0.0.1',
     description='Utilities for cleaning text',
     long_description=open('README.md').read().strip(),
     author='Koustuv Sinha',
     author_email='koustuvsinha@hotmail.com',
     url='https://github.com/koustuvsinha/swacch',
     packages=find_packages(),
     include_package_data=True,
     install_requires=['nltk','scikit-learn'],
     license='MIT License',
     zip_safe=False,
     test_suite='py.test',
     keywords='text utility',
     classifiers=[])
