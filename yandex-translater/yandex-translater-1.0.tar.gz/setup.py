from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yandex-translater',
    version='1.0',
    description='API for Yandex Translate',
    url='https://fossil.falseking.site/',
    author='James Axl',
    author_email='axlrose112@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='yandex-translater translater yandex translate',
    packages=find_packages(exclude=['examples', 'yandex_test.py']),
)

