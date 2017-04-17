# -*- coding: utf-8 -*-

"""Show help for specific command.

Usage:
    takumi help <command>
    takumi help -h | --help

Options:
    -h, --help      Show this message and exit
"""

from ._base import parse_args


def run(args):
    args = parse_args('help', __doc__, args, {'<command>': str})
    return args['<command>']
