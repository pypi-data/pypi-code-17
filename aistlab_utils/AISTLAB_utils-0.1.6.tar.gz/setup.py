# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aist_utils import (__author__, __description__, __email__, __license__,
                        __title__, __url__, __version__)

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=open('README.rst').read(),
    author=__author__,
    author_email=__email__,
    license=__license__,
    url=__url__,  # use the URL to the github repo
    download_url='https://github.com/winxos/AISTLAB_utils',
    keywords=['utils', 'winxos', 'AISTLAB'],  # arbitrary keywords
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
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
