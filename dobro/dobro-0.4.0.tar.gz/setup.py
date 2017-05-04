import os
from subprocess import check_output, CalledProcessError
from setuptools import setup

setup(
    name = "dobro",
    version = "0.4.0",
    author = "Douglas Thompson",
    author_email = "service+git@dougthompson.co.uk",
    description = ("Manage DigitalOcean droplets by tag"),
    license = "MIT",
    keywords = "digitalocean droplet cli doctl devops",
    url = "https://github.com/snoopdouglas/dobro",
    packages=['dobro'],
    entry_points = {
        'console_scripts': ['dobro=dobro.cli:main'],
    },
    long_description="Manage DigitalOcean droplets by tag. See: https://github.com/snoopdouglas/dobro",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ],
    test_suite='dobro.tests',
    zip_safe=False,
)
