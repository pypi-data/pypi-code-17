# -*- coding: utf-8; -*-

# This is part of weaklisp, a program for analysis of simple lisp
# code.

# Copyright (C) 2016, 2017 Yuri Teixeira

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.


from argparse import ArgumentParser
from pathlib import Path

from .formatter import format_lisp, format_conf
from .parser import parse


ENCODING = 'windows-1252'


def main():
    parser = ArgumentParser(prog='weaklisp',
                            description='Analyze simple lisp code.')
    parser.add_argument('path', nargs='+',
                        help='Path to lisp file to be parsed.')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Do not print the output.')
    parser.add_argument('-o', '--output', nargs=1,
                        help='Save a reStructuredText file.')
    parser.add_argument('-f', '--format', nargs='?', default='lisp',
                        help="Format of files, either 'lisp' or 'config'.")
    args = parser.parse_args()
    for path in args.path:
        path = Path(path)
        if args.format == 'lisp':
            formatted = format_lisp(parse(path)).encode().decode(ENCODING)
        else:
            formatted = format_conf(path)  #.encode().decode(ENCODING)
        if not args.quiet:
            print(formatted, '\n')
        if args.output:
            out = args.output[0]
            with open(out, 'w', encoding=ENCODING) as file:
                file.write(formatted)
            print('File created: {}'.format(out))


if __name__ == '__main__':
    main()
