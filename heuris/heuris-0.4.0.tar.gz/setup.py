from setuptools import setup
import sys

requirements = []

if sys.version_info < (3, 4):
    requirements.append('enum34')

config = {
    'name': 'heuris',
    'description': 'Python client for heuris',
    'author': 'Alex Young',
    'author_email': 'alex@heuris.io',
    'license': 'Apache License, Version 2.0',
    'url': 'https://github.com/heurisio/heuris-py',
    'version': '0.4.0',
    'install_requires': requirements,
    'packages': ['heuris']
}

setup(**config)
