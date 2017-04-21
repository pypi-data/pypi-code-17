#!/usr/bin/env python

import sys
import argparse

from . import flextableparser

def parse_args(argv):

    #print(argv)
    parser = argparse.ArgumentParser()
    parser.add_argument(
                        "input_file",
                        type = str,
                        help = 'Input file path')
    parser.add_argument(
                        "-d",
                        "--delimiter",
                        dest = "delimiter",
                        type = str,
                        help = "Use built-in table conversion schema",
                        required = False)

    if len(argv) < 1:
        print("No arguments specified")
        parser.print_help()
        sys.exit()
    args = parser.parse_args(argv)
    return(args)

def main():
    args = parse_args(sys.argv[1:])
    #print(args)
    if args.delimiter:
        flextableparser.transpose(args.input_file, args.delimiter)
    else:
        flextableparser.transpose(args.input_file)

if __name__ == '__main__':
    main()