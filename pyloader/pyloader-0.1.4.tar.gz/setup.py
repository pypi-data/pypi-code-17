import os
from setuptools import setup

try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = open(os.path.join(here, 'README.txt')).read()
except IOError:
    description = ''

version = "0.1.4"
dependencies = []

setup(name='pyloader',
      version=version,
      description="Load python attributes from a string",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://k0s.org/hg/pyloader',
      license='MPL',
      packages=['pyloader'],
      include_package_data=True,
      zip_safe=False,
      install_requires=dependencies,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      pyloader = pyloader.invoke:main
      """,
      )

