# -*- coding: utf-8 -*-

"""Takumi command line toolkit.

Usage:
    takumi <command> [<args>...]
    takumi -h | --help

Options:
    -h, --help      Show this message and exit
    --version       Show version

Commands:
    help            Show help for command
    run             Run script
    test            Run tests
    serve           Serve the service using gunicorn
    deploy          Deploy the service to an environment
    shell           Start an IPython REPL
"""

import sys
import schema
from docopt import DocoptExit
from ._base import parse_args

__version__ = '0.1.0'

commands = 'help', 'run', 'test', 'serve', 'deploy', 'shell'


def run(command, args):
    if command == 'help':
        from .help import run as help
        cmd = help(args)
        return run(cmd, ['-h'])
    if command == 'serve':
        from .serve import run as serve
        return serve(args)
    if command == 'deploy':
        from .deploy import run as deploy
        return deploy(args)
    if command == 'shell':
        from .shell import run as shell
        return shell(args)
    raise DocoptExit('Command {!r} not supported\n'.format(command))


def main():
    args = parse_args(None, __doc__, sys.argv[1:], {
        '<command>': schema.And(
            str, lambda c: c in commands,
            error='`<command>` should be one of {}'.format(commands)),
        '<args>': list,
    }, version=__version__, options_first=True)

    if '' not in sys.path:
        # Insert current directory
        sys.path.insert(0, '')
    run(args['<command>'], args['<args>'])
