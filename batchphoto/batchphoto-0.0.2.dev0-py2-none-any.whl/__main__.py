

# Import from the future for Python 2 and 3 compatability!
from __future__ import print_function, absolute_import, unicode_literals

import sys
import argparse

import batchphoto

def main():
    # parser
    parser = argparse.ArgumentParser(description='batchphoto')
    ARG = parser.add_argument

    ARG('action', action='store', nargs='?', default=None,
        help='action to perform')

    args, unknown = parser.parse_known_args()

    if args.action in batchphoto.__all__:
        __import__('.'.join(['batchphoto', args.action, '__main__']))
        getattr(batchphoto, args.action).__main__.main()
    else:
        print('Please provide a valid action to perform. Must be one of:\n',
              '\n'.join(batchphoto.__all__))
    sys.exit()

if __name__ == '__main__':
    main()
