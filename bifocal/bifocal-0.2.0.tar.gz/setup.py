import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='bifocal',
    version='0.2.0',
    author='James Prestwich',
    author_email='james@storj.io',
    description=('Automated FIFO and LIFO accounting for cryptocurrencies.'),
    license='AGPLv3+',
    keywords='accounting bitcoin FIFO LIFO cryptocurrency',
    url='https://github.com/frdwrd/bifocal',
    download_url='https://github.com/frdwrd/bifocal/archive/v0.1.1.tar.gz',
    packages=['bifocal'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Affero General Public License v3',
    ],
)
