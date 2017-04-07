import os
from setuptools import setup

CURRENT_VERSION = '0.0.3'


def read_file(filename):
    """Open a file, read it and return its contents."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()

setup(
    name='knot-injector',
    version=CURRENT_VERSION,
    description='Framework agnostic dependency injections',

    # Get the long description from the README file
    long_description=read_file('README.rst'),

    url='https://github.com/rdidyk/knot-injector',
    download_url='https://github.com/rdidyk/knot-injector/archive/{}.tar.gz'.format(CURRENT_VERSION),

    author='Ruslan Didyk',
    author_email='rdidyk@tmgtop.com',
    license='MIT',

    classifiers=[
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='dependencies injection',
    packages=['knot_injector'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'knot',
    ],

    package_data={
        'knot_injector': [
            'README.rst',
            'setup.cfg',
            'LICENSE',
            'requirements.txt',
        ],
    }
)
