#coding=utf8

from setuptools import setup, find_packages

setup(
    name = "QCloudChameleon",
    version = "0.1.0",
    packages = find_packages(),
    include_package_data = True,
    package_data = {'bwmodel':['./chameleon/core/resources/*/*.*']},

    description = "a DSL tool to generate Objective-C model code",
    long_description = "a DSL tool to generate Objective-C model code, it base antrl4 and python",
    author = "yishuiliunian",
    author_email = "yishuiliunian@gmail.com",

    license = "GPL",
    keywords = ("Objective-C", "DSL", "model"),
    platforms = "any",
    url = "http://www.github.com/yishuiliunian",
    scripts=['bin/chameleon'],
    #dependency
    install_requires=['mako', 'antlr4-python2-runtime'],
)
