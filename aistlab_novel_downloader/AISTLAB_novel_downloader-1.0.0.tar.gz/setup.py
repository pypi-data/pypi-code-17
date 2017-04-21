# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from novel_downloader import (__author__, __description__, __long_description__, __email__, __license__,
                        __title__, __url__, __version__)

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=__long_description__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    url=__url__,  # use the URL to the github repo
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['aistlab_novel_grab'],
    packages=find_packages(),
    package_dir={'novel_downloader': 'novel_downloader'},
    entry_points={
        "console_scripts": [
            "novel_service = novel_downloader.novel_downloader:main",
        ]
    }
)
