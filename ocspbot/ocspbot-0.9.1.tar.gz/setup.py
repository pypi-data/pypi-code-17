"""OCSP Bot"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ocspbot',
    version='0.9.1',
    description='Ensure up-to-date OCSP responses for certificates are available.',
    long_description=long_description,
    url='https://github.com/felixfontein/ocspbot',
    author='Felix Fontein',
    author_email='felix@fontein.de',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Security',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ocsp response update',
    packages=find_packages(),
    install_requires=['setuptools>=20.3', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'ocspbot = ocspbot.__main__:main',
        ],
    },
)
