from distutils.core import setup
setup(
  name = 'mnis',
  packages = ['mnis'],
  version = '1.0.14',
  description = 'A small library that makes it easy to download data on UK Members of Parliament',
  author = 'Oliver Hawkins',
  author_email = 'oli@olihawkins.com',
  url = 'https://github.com/olihawkins/mnis',
  download_url = 'https://github.com/olihawkins/mnis/tarball/1.0.14',
  keywords = ['MPs', 'Parliament', 'House of Commons'],
  install_requires = ['requests'],
  classifiers = [],
)