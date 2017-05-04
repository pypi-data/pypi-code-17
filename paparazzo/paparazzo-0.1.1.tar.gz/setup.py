from setuptools import setup
import re

with open('paparazzo/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='paparazzo',
    packages=[
        'paparazzo'
    ],
    version=version,
    description='Paparazzo is a tool for the automation of Elasticsearch data backup and restoration,'
                ' utilising Amazon\'s S3.',
    author='Ethan Bray',
    author_email='e.bray@txtnation.com',
    url='https://github.com/ethanbray/paparazzo',
    download_url='https://github.com/ethanbray/paparazzo/archive/0.1.1.tar.gz',
    keywords=[
        'elasticsearch',
        'snapshot',
        'backup'
    ]
)
