#!/usr/bin/env python

from setuptools import setup

setup(name='tap-freshdesk',
      version='0.6.7',
      description='Singer.io tap for extracting data from the Freshdesk API',
      author='Stitch',
      url='http://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_freshdesk'],
      install_requires=[
          'singer-python>=0.2.1',
          'requests==2.12.4',
      ],
      entry_points='''
          [console_scripts]
          tap-freshdesk=tap_freshdesk:main
      ''',
      packages=['tap_freshdesk'],
      package_data = {
          'tap_freshdesk/schemas': [
              'agents.json',
              'companies.json',
              'contacts.json',
              'conversations.json',
              'groups.json',
              'roles.json',
              'satisfaction_ratings.json',
              'tickets.json',
              'time_entries.json',
          ],
      },
      include_package_data=True,
)
