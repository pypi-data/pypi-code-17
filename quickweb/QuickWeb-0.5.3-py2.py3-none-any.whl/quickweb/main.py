#! /usr/bin/env python

"""QuickWeb

Usage:
    quickweb init <app_directory> <template_name> [--force]
    quickweb create <url> [<app_directory>] [--force]
    quickweb run [<app_directory>]

Examples:

    quickweb init my-first-app bootstrap-starter
    quickweb create https://getbootstrap.com/examples/starter-template/

Options:
  -h --help     Show this screen.
"""
import os
import sys
from os.path import join, dirname

from docopt import docopt

# Make sure we use the source directory for imports when running during development
script_dir = join(dirname(os.path.realpath(__file__)), '..')
sys.path.insert(0, script_dir)


from quickweb import appmanager
from quickweb.templatemanager import TemplateMaker


def main():
    arguments = docopt(__doc__, version='QuickWeb (latest)')

    if arguments['create']:
        TemplateMaker(arguments['<url>'], arguments['<app_directory>']).make(arguments['--force'])

    if arguments['init']:
        appmanager.init(arguments['<app_directory>'], arguments['<template_name>'], arguments['--force'])

    if arguments['run']:
        appmanager.run(arguments['<app_directory>'])

if __name__ == "__main__":
    main()
