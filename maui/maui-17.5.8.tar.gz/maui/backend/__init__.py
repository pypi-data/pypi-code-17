# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import argparse
import logging

cli = argparse.ArgumentParser(add_help=False)
cli.add_argument('-h', '--help', action='store_true', help='show this help message')

from maui.backend.serial.context import SerialContext

def guess_context(cli):

    verbosity_group = cli.add_mutually_exclusive_group()
    verbosity_group.add_argument("--verbose", "-v", action="count")
    verbosity_group.add_argument("-q", "--quiet", action="store_true")

    args, unknown = cli.parse_known_args()

    try:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        if size>1:
            from maui.backend.mpi.context import MPIContext
            return MPIContext(), args, unknown
        else:
            return SerialContext(), args, unknown
    except:
        return SerialContext(), args, unknown


logger = logging.getLogger(__name__)
context, args, arguments = guess_context(cli)
stdout = context.stdout
stderr = context.stderr

if args.help:
    cli.print_help(file=stderr)
    import sys
    sys.exit()

try:
    from nicelog.formatters import ColorLineFormatter
    handler = logging.StreamHandler(stdout)
    handler.setFormatter(ColorLineFormatter(show_date=True, show_function=True, show_filename=True, message_inline=True))
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
except ImportError:
    handler = logging.StreamHandler(stdout)
    log_string = '[%(asctime)s] %(levelname)s <%(name)s> "%(message)s"'
    formatter = logging.Formatter(fmt=log_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.setLevel(logging.DEBUG)

if isinstance(context, SerialContext):
    logger.info("Running MAUI with serial backend.")
else:
    logger.info("Running MAUI with MPI backend.")

