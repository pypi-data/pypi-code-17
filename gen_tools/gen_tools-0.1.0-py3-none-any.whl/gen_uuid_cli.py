#!/usr/bin/env python3.6

import sys
import uuid


def gen_uuid(capitalize: bool = False) -> str:
    """
    Return random UUID. If capitalize is True then use upper case for letters.

    :param capitalize: whether or not to use upper case letters.
    :return: generated UUID as str.
    """

    if capitalize:
        resp = str(uuid.uuid4()).upper()
    else:
        resp = str(uuid.uuid4())

    return resp


def main():
    sys.stdout.write(gen_uuid())

if __name__ == '__main__':
    main()
