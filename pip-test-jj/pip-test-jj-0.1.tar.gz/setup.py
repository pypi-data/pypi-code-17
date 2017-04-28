try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(
  name = 'pip-test-jj',
  packages = ['pip-test-jj'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test pip lib',
  author = 'JJ',
  author_email = 'jjuhn1119@gmail.com',
  url = 'https://github.com/jjuhn/pip-test-jj',
  download_url = 'https://github.com/jjuhn/pip-test-jj/archive/master.zip',
  keywords = ['testing', 'example', 'pip'],
  classifiers = [],
)