# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version = '0.3b2'

install_requires = [
    'wsgistate >= 0.4.3',
    'setuptools',
    'transaction',
    'cromlech.browser >= 0.5.2',
    ]

tests_require = [
    'WebTest',
    ]

setup(name='cromlech.wsgistate',
      version=version,
      description="Session handling for cromlech using wsgistate",
      long_description=(
          open("README.txt").read() + "\n" +
          open(os.path.join("src", "cromlech", "wsgistate",
                            "test_session.txt")).read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Cromlech Wsgistate Session',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org/',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['cromlech',],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      [paste.filter_app_factory]
      session = cromlech.wsgistate.middleware:session_wrapper
      file_session = cromlech.wsgistate.middleware:file_session_wrapper
      """,
      )
