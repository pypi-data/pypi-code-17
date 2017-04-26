#!/usr/bin/env python3.6

import sys

from gen_tools.tools import gen_pass


def main(password_length: int = 8):
    sys.stdout.write(gen_pass(password_length))


if __name__ == '__main__':
    try:
        main(int(sys.argv[1]))
    except IndexError as e:
        main()
