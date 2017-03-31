from setuptools import setup
setup(
  name = 'jackster',
  packages = [
    'jackster',
    'jackster.funcs',
  ],
  package_dir = {
    'jackster': 'jackster',
    'jackster.funcs': 'jackster/funcs',
    'jackster.funcs.templates': 'jackster/funcs/templates',
  },
  license = 'MIT',
  version = '0.3.3',
  description = 'A micro web framework.',
  author = 'Daan van der Kallen',
  author_email = 'mail@daanvdk.com',
  url = 'https://github.com/Daanvdk/jackster', # use the URL to the github repo
  download_url = 'https://github.com/Daanvdk/jackster/archive/0.3.tar.gz', # I'll explain this in a second
  keywords = ['web', 'framework'], # arbitrary keywords
  classifiers = [],
  install_requires = [
    'jinja2',
  ],
)
