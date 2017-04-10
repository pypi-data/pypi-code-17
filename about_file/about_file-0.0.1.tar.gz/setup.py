#!/usr/bin/env python3

from distutils.core import setup

version = "0.0.1"

setup(
    name = 'about_file',
    packages = ['about'],
    license = 'MIT',
    version = version,
    description = 'About is a note tool that helps you describe files in your project.',
    author = 'Manoel Carvalho',
    author_email = 'manoelhc@gmail.com',
    url = 'https://github.com/manoelhc/about',
    download_url = 'https://github.com/manoelhc/about',
    keywords = ['testing', 'configuration'],
    install_requires=[
        'homer'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
            'console_scripts': [
                'about=about:main',
            ],
    }
)
