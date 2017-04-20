from setuptools import setup

url = "https://github.com/JIC-CSB/dtoolutils"
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtoolutils",
    packages=["dtoolutils"],
    version=version,
    description="Utilities for working with dtoolcore",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    install_requires=[
        "binaryornot",
        "dtoolcore",
        "puremagic",
    ],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT")
