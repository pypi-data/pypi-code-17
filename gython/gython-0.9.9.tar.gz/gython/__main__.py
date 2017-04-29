#!/usr/bin/env python

import sys

from .translator import command


def main():
    sys.argv = [sys.argv[0], '--go'] + sys.argv[1:]
    command()
