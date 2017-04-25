from setuptools import find_packages
from setuptools import setup

setup(
    name="j2s",

    version="1.0.1",

    description="convert a json dictionary to a swagger definition",

    url="https://github.com/af-inet/j2s",

    author="David Hargat",

    author_email="davidmhargat@gmail.com",

    license="MIT",

    keywords="json to swagger",

    packages=find_packages(),

    install_requires=[],

    scripts=['bin/j2s']
)
