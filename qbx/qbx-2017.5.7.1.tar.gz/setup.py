from setuptools import setup

from sys import platform

if platform == 'win32':
    script = 'bin/qbx.cmd'
else:
    script = 'bin/qbx'
setup(name='qbx',
      author='qbtrade',
      url='https://github.com/qbtrade/qbx',
      author_email='admin@qbtrade.org',
      packages=['qbx'],
      version='2017.5.7.1',
      install_requires=[
          'docopt',
          'requests'
      ],
      zip_safe=False,
      scripts=[
          script
      ]
      )
