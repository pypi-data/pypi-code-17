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
  version = '0.4.1',
  description = 'A micro web framework.',
  author = 'Daan van der Kallen',
  author_email = 'mail@daanvdk.com',
  url = 'https://github.com/Daanvdk/jackster',
  download_url = 'https://github.com/Daanvdk/jackster/archive/0.4.tar.gz',
  keywords = ['web', 'framework'],
  classifiers = [],
  install_requires = [
    'werkzeug',
    'jinja2',
  ],
)
