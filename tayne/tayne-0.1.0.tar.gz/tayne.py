#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2017, Eddie Antonio Santos <easantos@ualberta.ca>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


"""
tayne - companion for entr(1)

Usage:
    tayne [--print]
    tayne (-h | --help)
    tayne --version

Options:
    -h --help   Show this screen.
    --version   Show version
"""

import configparser
import glob
import os
import sys
import subprocess

import docopt  # type: ignore


__package__ = 'tayne'
__semantic_version__ = 0, 1, 0
__version__ = '.'.join(map(str, __semantic_version__))


TEST_CONFIG = """
[tayne]
patterns =
    **/*.py
    **/*.ini
command = py.test tayne.py
entr_opts = -c
"""


def test():
    pass


def outputting_to_terminal():
    return os.isatty(sys.stdout.fileno())


def print_files(filenames):
    for filename in filenames:
        print(filename)


def main() -> None:
    # Parse args
    arguments = docopt.docopt(__doc__, version=f"{__package__} {__version__}")

    # Read config
    config = configparser.ConfigParser()
    config.read('.taynerc', encoding='UTF-8')
    tayne = config['tayne']

    # Get list of files
    patterns = tayne['patterns'].split()
    files = [filename for pattern in patterns
             for filename in glob.iglob(pattern, recursive=True)]
    assert not any('\n' in filename for filename in files)

    if arguments['--print'] or not outputting_to_terminal():
        print_files(files)
    else:
        options = tayne.get('entr_opts', '').split()
        cmd = tayne['command']
        subprocess.run([
            'entr', *options, 'sh', '-c', cmd
        ], encoding='UTF-8', input='\n'.join(files))


if __name__ == '__main__':
    main()
