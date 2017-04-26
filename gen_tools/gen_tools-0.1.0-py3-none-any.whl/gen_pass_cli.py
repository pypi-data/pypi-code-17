#!/usr/bin/env python3.6

import secrets
import string
import sys


def gen_pass(pass_length: int = 8) -> str:
    """
    Return random alphanumeric str with a length of pass_length.

    :param pass_length: length of returned password.
    :return: generated password as str.
    """

    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphanumeric_chars)
                   for i in range(pass_length))


def main(password_length: int = 8):
    sys.stdout.write(gen_pass(password_length))


if __name__ == '__main__':
    try:
        main(int(sys.argv[1]))
    except IndexError as e:
        main()
