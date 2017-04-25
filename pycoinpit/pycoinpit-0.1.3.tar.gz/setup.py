#!/usr/bin/env python
from distutils.core import setup
setup(
  name = 'pycoinpit',
  packages = ['pycoinpit'], # this must be the same as the name above
  scripts = ['coinpit.py'],
  install_requires=[ "pybitcointools", "pyelliptic==1.5.7", "requests" ],
  version = '0.1.3',
  description = 'Coinpit Python Client',
  author = 'Coinpit',
  author_email = 'info@coinpit.io',
  url = 'https://github.com/coinpit/pycoinpit', # use the URL to the github repo
  download_url = 'https://github.com/coinpit/pycoinpit/tarball/0.2',
  keywords = ['coinpit', 'trading', 'python'],
  classifiers = [],
)

# Register package with pypi
#  setup.py register
# Build:
#  python setup.py sdist
# To publish on test:
#  twine upload dist/pycoinpit-0.3.1.tar.gz -r pypitest
# To install test
#  pip install -i https://testpypi.python.org/pypi pycoinpit
#
# To publish production
#  twine upload dist/pycoinpit-0.3.1.tar.gz -r pypi
# To install production
#  pip install pycoinpit
