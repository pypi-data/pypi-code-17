# -*- coding: utf-8 -*-
# from distutils.core import setup
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='AISTLAB_utils',
    version='0.1',
    description='Utils',
    long_description=long_description,
    author='winxos',
    author_email='winxos@hotmail.com',
    url='https://github.com/winxos/AISTLAB_utils',  # use the URL to the github repo
    download_url='https://github.com/winxos/AISTLAB_utils',
    keywords=['utils', 'winxos', 'AISTLAB'],  # arbitrary keywords
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # install_requires=[''],
    packages=find_packages(),
    package_dir={'aist_utils': 'aist_utils'},
    entry_points={
        "console_scripts": [
            "aistlab = aist_utils.AISTLAB:about_aistlab",
            "purge = aist_utils.creo:purge",
        ]
    }
)
