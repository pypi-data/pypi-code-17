# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from nitrotyper import (__author__, __description__, __email__, __license__,
                        __title__, __url__, __version__)

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    url=__url__,  # use the URL to the github repo
    keywords=['nitrotype', 'winxos', 'AISTLAB'],  # arbitrary keywords
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['pyautogui', 'opencv-python'],
    packages=find_packages(),
    package_dir={"nitrotyper": "nitrotyper"},
    package_data={
        "nitrotyper": ["data/*.json"]
    },
    entry_points={
        "console_scripts": [
            "nitrotyper = nitrotyper.nitrotyper:run",
        ]
    }
)
