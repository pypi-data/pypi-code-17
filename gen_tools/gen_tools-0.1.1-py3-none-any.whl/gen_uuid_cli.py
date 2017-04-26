#!/usr/bin/env python3.6

import sys

from gen_tools.tools import gen_uuid


def main(use_caps: bool = False):
    sys.stdout.write(gen_uuid(capitalize=use_caps))

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError as e:
        main()
