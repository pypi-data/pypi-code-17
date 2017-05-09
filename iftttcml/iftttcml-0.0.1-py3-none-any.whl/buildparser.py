# -*- coding: utf-8 -*-

import argparse
import os

from iftttcml import __version__


def build_parser():
    """ Parser args """
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--maker', type=str,
                        dest='maker', default=None,
                        help='Maker python file')

    parser.add_argument('-p', '--params', type=str,
                        dest='params', default=None,
                        help='Params for Maker in JSON')

    parser.add_argument('-k', '--key', type=str,
                        dest='key', default=os.environ.get('IFTTT_API_KEY'),
                        help='IFTTT API key')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    return parser
