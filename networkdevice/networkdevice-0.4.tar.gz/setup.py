#!/usr/bin/env python

from setuptools import setup

setup(name='networkdevice',
      version='0.4',
      author='Yongping Guo',
      author_email='guoyoooping@163.com',
      description='Python modules to execut command on remote network device based on pexpect.',
      long_description=open('README.rst').read(),
      install_requires = ["pexpect", "xmltodict"],
      url='https://github.com/guoyoooping/networkdevice',
      license="GPLv3",
      scripts=['demo/ftp_test.py'],
      packages=['networkdevice']
      )
