import os
import re
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = ''
with open('finsym/version.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

AUTHOR = 'Aquil H. Abdullah'
EMAIL = 'aquil.abdullah@lgmail.com'
REQUIRES = ['singledispatch']

setup(
    name='finsym',
    version=version,
    author=AUTHOR,
    author_email=EMAIL,
    packages=['finsym'],
    package_data={'finsym': ['README.md']},
    url='https://github.com/aabdullah-bos/finsym',
    download_url='https://github.com/aabdullah-bos/finsymarchive/0.0.2.tar.gz',
    description='Package for representing financial symbols',
    long_description=read('README.md'),
    install_requires=REQUIRES
)
