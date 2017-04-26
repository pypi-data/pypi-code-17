"""
Copyright (c) 2016 we-get developers (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying permission
"""

from setuptools import setup, find_packages
version = '1.0.1'

setup(
    name='we-get',
    version=version,
    description='Search torrents from the command-line',
    author='Levi Sabah',
    author_email='x@levisabah.com',
    license='MIT',
    keywords=['command line', 'torrent', 'torrents', 'magnet'],
    url='https://github.com/levisabah/we-get',
    packages=find_packages(),
    install_requires=['docopt', 'prompt_toolkit', 'colorama'],
    include_package_data=True,
    package_data={'we_get': ['extra/useragents.txt']},
    entry_points={'console_scripts': ['we-get=we_get:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    
    ],
)
