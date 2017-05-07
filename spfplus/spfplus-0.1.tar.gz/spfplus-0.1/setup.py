"""
Setup file for pip.
"""

from distutils.core import setup

setup(
    name='spfplus',
    packages=['spfplus'], # this must be the same as the name above
    version='0.1',
    description='Sender Policy Framework (SPF) python library.',
    author='Hang Hu',
    author_email='theodorehu95@gmail.com',
    url='https://github.com/theodorehu95/spfplus', # use the URL to the github repo
    download_url='https://github.com/theodorehu95/spfplus/archive/{tag}.tar.gz', # I'll explain this in a second
    keywords=['spf', 'email', 'authentication'], # arbitrary keywords
    classifiers=[],
)