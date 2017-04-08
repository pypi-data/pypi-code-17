# -*- coding: utf-8 -*-

"""
sqloose CLI interface.

Usage:
    cli.py [INDEX ...]

Options:
    -h --help               Show this screen.
    --version               Show version.
"""

import os
import sys
import docopt

CURRENT_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_DIR, "..")))

import sqloose
from sqloose import __version__

def main():
    """Console script for sqloose"""
    args = docopt.docopt(__doc__, version=__version__)

    for item in args['INDEX']:
        print(sqloose.to_sql(item))

if __name__ == "__main__":
    main()
