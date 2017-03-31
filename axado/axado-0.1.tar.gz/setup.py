from setuptools import setup

setup(
  name = 'axado',
  packages = ['axado'],
  version = '0.1',
  description = 'Python bindings to the Axado API (https://developers.axado.com.br/)',
  author = 'Paulo Scardine',
  author_email = 'paulos@xtend.com.br',
  url = 'https://github.com/scardine/python-axado',
  download_url = 'https://github.com/scardine/python-axado/archive/0.1.tar.gz',
  keywords = ['axado', 'api'],
  classifiers = [],
  install_requires=[
    'requests',
  ],
)