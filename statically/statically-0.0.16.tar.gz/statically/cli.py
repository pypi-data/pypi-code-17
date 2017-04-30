#!/usr/bin/env python3

import statically
from statically import update
from statically import init

import argparse
import os
from pathlib import Path
import argcomplete

def parse_args():

    """parse command line arguments"""

    parser = argparse.ArgumentParser(description="Static site generator with markdown.")
    subparsers = parser.add_subparsers(help='command help')

    parser_init = subparsers.add_parser('init', help='Initializa a new statically instance')
    parser_init.add_argument('path', type=str, help='new statically instance path')
    parser_init.set_defaults(func=init)


    parser_update = subparsers.add_parser('update', help='Generate webpage')
    parser_update.add_argument('path', type=str, help='path to statically instance')
    parser_update.set_defaults(func=update)

    argcomplete.autocomplete(parser)
    return parser.parse_args()


def main(args):
    path = Path(args.path)
    url = "https://api.github.com/repos/joajfreitas/statically-minimal/tarball/master"

    args.func(path, url)


def run():
    main(parse_args())
