#!/usr/bin/env python
# coding=utf-8

"""The Mal Language Parser and Runtime Environment main script

"""
from __future__ import print_function

import getopt
import sys

from random import shuffle

import malpy.cycleanalyzer
import malpy.parser


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def call(opts, args):
    """main loop

    return:
        None

    """
    parser = malpy.parser.Parser()
    runner = malpy.cycleanalyzer.CycleAnalyzer()

    opts = dict(opts or [])
    for arg in args:
        memory = []
        if "-m" in opts or "--memory" in opts:
            try:
                memory = list(map(int,
                                  opts.get("-m", opts.get("--memory", ""))
                                  .split()))
            except Exception as err:

                print(err)
        if len(memory) != 64:
            memory = list(range(64))
            shuffle(memory)
        token_ast = parser.parse(open(arg).read())
        if not any([token[0] == 'E' for token in token_ast]):
            output = runner.run(token_ast, memory)
            print(output)

    return 0


def main(argv=None):
    """main runner

    return:
        None

    """
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hm:", ["help", "memory="])
        except getopt.error as msg:
            raise Usage(msg)

        return call(opts, args)

    except Usage as err:
        print(err.msg, file=sys.stderr)
        print("For help, use --help", file=sys.stderr)
        return 127


if __name__ == '__main__':
    sys.exit(main())
