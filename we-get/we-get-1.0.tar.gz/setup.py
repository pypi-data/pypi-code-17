"""
Copyright (c) 2016 we-get developers (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying permission
"""


from setuptools import setup, find_packages
version = '1.0'

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
    package_data={'we_get': ['txt/useragents.txt']},
    entry_points={'console_scripts': ['we-get=we_get:main']},
    download_url = 'https://github.com/levisabah/we-get/archive/1.0.tar.gz',
)
