# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import sys
import six

from .pdb import Protein

from . import __version__



# Main parser
parser = argparse.ArgumentParser(
    description="A docking utility made for the M1 BIBS Python course."
)
parser.add_argument(
    '--version', action='version',
    version='dockerasmus v{}'.format(__version__),
)

# Subparsers
subparsers = parser.add_subparsers(dest="cmd")
subparsers.required = True

## Subparser: Generate
parser_gen = subparsers.add_parser('generate')
parser_gen.add_argument(
    'static', type=Protein.from_pdb_file,
    help='the path to a pdb file containing the static component'
         ' of the complex (receptor)',
)
parser_gen.add_argument(
    'mobile', type=Protein.from_pdb_file,
    help='the path to a pdb file containing the mobile component'
         ' of the complex (ligand)',
)
parser_gen.add_argument(
    '--out', type=six.text_type, metavar="OUTDIR",
    help="the path to the output directory [default: .]",
    default=".",
)
