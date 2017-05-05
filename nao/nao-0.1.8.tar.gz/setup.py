from distutils.core import setup
setup(
  name = 'nao',
  packages = ['nao'],
  version = '0.1.8',
  description = 'Intelligent data manipulation tools',
  author = 'Szabolcs Blaga',
  author_email = 'szabolcs.blaga@gmail.com',
  url = 'https://github.com/blagasz/nao',
  download_url = 'https://github.com/blagasz/nao/tarball/0.1',
  license = 'GPL',
  install_requires=[
    'PyYAML',
    'numpy==1.11.1',
    'pandas==0.18.1',  # for datetime conversion and distinct
  ],
  keywords = ['data', 'yaml', 'multilingual', 'multivalue', 'config'],
  classifiers = [],
)