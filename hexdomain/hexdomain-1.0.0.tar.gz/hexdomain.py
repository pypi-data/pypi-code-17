"""
Generate domain names that only contain hexadecimal numbers.
"""

from __future__ import print_function

import argparse
import string
import sys
import textwrap

from six.moves import reduce
import tld

__version__ = '1.0.0'

HEX_SUBSTITUTIONS = [
    ('ate', '8'),
    ('ude', '00d'),
    ('g', '6'),
    ('l', '1'),
    ('o', '0'),
    ('s', '5'),
    ('t', '7'),
]
HEX_SUBSTITUTION_TABLE = '\n'.join('    {}\t{}'.format(chars, substitution)
                                   for chars, substitution in HEX_SUBSTITUTIONS)

ALLOWED_CHARS = string.hexdigits + '.'

HEX_TLDS = set(name for name in tld.get_tld_names()
               if all(char in ALLOWED_CHARS for char in name))


class ParseReplacementsFileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        substitutions = list(parse_substitutions(values))
        setattr(namespace, 'substitutions', substitutions)


def words(filename):
    with open(filename) as word_file:
        for word in word_file:
            yield word.strip()


def replace_multiple(word, substitutions):
    def replace(word, pair):
        return word.replace(*pair)
    return reduce(replace, substitutions, word)


def hexspeak(word, substitutions):
    return replace_multiple(word, substitutions)


def hex_domains(filename, substitutions):
    for word in words(filename):
        hexed = hexspeak(word, substitutions)
        if not all(char in string.hexdigits for char in hexed):
            continue
        if hexed[-2:] in HEX_TLDS:
            domain = hexed[:-2] + '.' + word[-2:]
            yield word, domain


def parse_substitutions(filename):
    with open(filename) as substitutions_file:
        for line in substitutions_file:
            char, substitution = line.strip().split(None, 1)
            yield char, substitution


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=textwrap.dedent('''
        DEFAULT SUBSTITUTIONS

        {}

        SUBSTITUTION FILE SYNTAX

        You can override the default hexspeak substitutions using a simple
        whitespace-delimited text file:

            <character(s)>  <substitution>

        %(prog)s will apply each substitution in order. In general, you will
        want to replace longer strings before individual characters as shown
        above.
        ''').format(HEX_SUBSTITUTION_TABLE),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('words', nargs='?', default='/usr/share/dict/words',
                        help='Path to words file [%(default)s]')
    parser.add_argument(
        '-f', '--substitutions-file',
        help='Path to substitutions file',
        dest='substitutions',
        action=ParseReplacementsFileAction,
        default=HEX_SUBSTITUTIONS,
    )
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    return parser.parse_args()


def main(argv=None):
    argv = argv if argv else sys.argv[1:]
    args = parse_args(argv)
    substitutions = args.substitutions if args.substitutions else HEX_SUBSTITUTIONS
    for word, domain in hex_domains(args.words, substitutions):
        print(word, '\t', domain)


if __name__ == '__main__':
    sys.exit(main())
