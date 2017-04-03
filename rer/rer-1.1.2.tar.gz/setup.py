"""Regular expression in regular expression

Ref:
https://github.com/jks-liu/rere
"""

from os import path
from setuptools import setup, find_packages

MODULE_PATH = path.abspath(path.dirname(__file__))

with open(path.join(MODULE_PATH, 'README.txt')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='rer',
    version='1.1.2',
    description='Regular expression in regular expression',
    long_description=LONG_DESCRIPTION,

    url='https://github.com/jks-liu/rere',

    author='Meme Kagurazaka',
    author_email='github@mrliu.org',

    license='Public Domain',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # Pick your license as you wish (should match "license" above)
        'License :: Public Domain',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='Nested regular expression re',

    packages=find_packages(),
)
