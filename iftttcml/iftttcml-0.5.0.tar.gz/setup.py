# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import iftttcml

setup(
    name='iftttcml',
    version=iftttcml.__version__,
    packages=find_packages(),
    author='penicolas',
    author_email='png1981@gmail.com',
    description='ITFFF: custom maker launcher',
    long_description="README on github : https://github.com/penicolas/iftttcml",
    install_requires=['metrovlc'],
    url='https://github.com/penicolas/ifttt-cml',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'iftttcml = iftttcml.iftttcml:main',
        ],
    },
)
