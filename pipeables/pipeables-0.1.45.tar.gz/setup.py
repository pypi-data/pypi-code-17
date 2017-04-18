from setuptools import setup

import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test*.py')
    return test_suite

setup(name='pipeables',
      version='0.1.45',
      description='Simiple queries and piping between different data sources',
      url='https://bitbucket.org/tdoran/pipeables/branch/v2package',
      author='Tony Doran',
      author_email='tdoran@atlassian.com',
      license='MIT',
      packages=['pipeables'],
      test_suite="setup.my_test_suite",
      entry_points={
          'console_scripts': [
              'pipeable=pipeables.command_line:pipeable',
              'makeList=pipeables.command_line:makeList',
              'makeValueList=pipeables.command_line:makeValueList',
              'intersection=pipeables.command_line:intersection'
          ]
      },
      install_requires=[
          'gdata',
          'pygresql==4.1.1',
          'googleads==4.2.0',
          'xmlrunner==1.7.7',
          'PyHive==0.2.1',
          'thrift==0.10.0',
          'sasl==0.2.1',
          'thrift-sasl==0.2.1',
          'JayDeBeApi==0.2.0',
          'requests'
      ],
      dependency_links = ['https://github.com/tdawber/jaydebeapi'],
      zip_safe=False)
