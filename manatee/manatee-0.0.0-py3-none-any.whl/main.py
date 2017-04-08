import sys
import logging
import argparse


def get_logger():
    return logging.getLogger()


def get_arg_parser():
    return argparse.ArgumentParser(
    )


def _main(argv):
    parser = get_arg_parser()
    logger = get_logger()
    args = parser.parse_args(argv)
    return 0


def main():
    status = _main(sys.argv)
    sys.exit(status)
