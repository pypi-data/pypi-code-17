from setuptools import setup

# import winger

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

NAME = 'winger'


DESCRIPTION = 'A Python3 module defines dict-like classes to handle Windows registry'


URL = 'https://github.com/meng89/' + NAME

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name=NAME,
      # version=winger.__version__,
      version='0.0.2',
      description=DESCRIPTION,
      include_package_data=True,
      author='Chen Meng',
      author_email='ObserverChan@gmail.com',
      license='LGPL v3.0',
      url=URL,
      py_modules=[NAME],
      install_requires=requirements,
      classifiers=CLASSIFIERS)
