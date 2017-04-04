from setuptools import setup

setup(
    name     = 'bunk',
    packages = ['bunk',],
    version  = '0.1.2',
    description = 'templating and environment management for kubernetes manifests',
    license  = 'MIT',
    scripts  = ['bin/bunk',],
    author   = 'Radek Goblin Pieczonka',
    author_email = 'goblin@pentex.pl',
    url = 'https://github.com/goblain/bunk',
    download_url = 'https://github.com/goblain/bunk/tarball/0.1.2.tar.gz',
    keywords = ['kubernetes', 'templates', 'environment'],
    classifiers = [],
    install_requires=[
      'PyYAML',
      'boto',
      'Jinja2',
      'hvac'
    ]
)
