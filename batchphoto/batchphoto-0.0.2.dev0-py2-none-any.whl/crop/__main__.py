# Import from the future for Python 2 and 3 compatability!
from __future__ import print_function, absolute_import, unicode_literals
import argparse
import batchphoto.crop as crop

def main():

    # parser
    parser = argparse.ArgumentParser(description='crop')
    ARG = parser.add_argument

    ARG('action', action='store', nargs='?', default=None,
        help='action to perform')
    ARG('method', action='store', nargs='?', default=None,
        help='method to use when cropping')

    args = parser.parse_args()

    if args.method in crop.__all__:
        print('cool')
    else:
        print('Please provide a valid method to use. Must be one of:\n',
              '\n'.join(crop.__all__))

if __name__ == '__main__':
    main()
