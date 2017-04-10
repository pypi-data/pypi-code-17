#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "NM53",
        version          = "2017.04.10.1824",
        description      = "create and update backups of GitHub repositories of a user",
        long_description = long_description(),
        url              = "https://github.com/wdbm/NM53",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "NM53"
                           ],
        install_requires = [
                           "docopt"
                           ],
        scripts          = [
                           "NM53"
                           ],
        entry_points     = """
            [console_scripts]
            NM53 = NM53:NM53
        """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
