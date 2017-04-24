from setuptools import setup

import glob

setup(
    name = 'finoex',
    version = '0.7.1',
    # description = '',
    author = 'Fabian Peter Hammerle',
    author_email = 'fabian.hammerle@gmail.com',
    url = 'https://git.hammerle.me/fphammerle/finoex',
    download_url = 'https://git.hammerle.me/fphammerle/finoex/archive/0.7.0.tar.gz',
    keywords = ['finances'],
    # classifiers = [],
    packages = ['finoex'],
    # scripts = glob.glob('scripts/*'),
    install_requires = [
        'ioex>=0.10.1',
        'pytz',
        ],
    tests_require = ['pytest'],
    )
