"""Entry point for pylint-ci
    Argparse is handled in the __main__.py to keep clutter out of other files
"""
import logging
import argparse
import sys
import pylint_ci

LOGGER = logging.getLogger('pylint_ci')
### Argument Parsing Initialization
PARSER = argparse.ArgumentParser(description='Utility to add Pass/Fail output on top of Pylint for version management purposes')
PARSER.add_argument('-v', '--verbosity',
                    metavar='LEVEL',
                    help='Specify level of verbosity for output',
                    type=int,
                    choices=range(0, 6),
                    default=2
)
PARSER.add_argument('target',
                    help='Specify a target on which the program will be run',
                    type=str,
                    nargs='*',
                    default=['.'],
)
PARSER.add_argument('-e', '--exclude',
                    help='Specify errors for pylint to ignore',
                    type=str,
                    nargs='*',
                    default=[''],
)
PARSER.add_argument('-i', '--ignore', # Maybe add a .pylintignore file to read
                    help='Specify files to ignore',
                    type=str,
                    nargs='*',
                    default=[''],
)
TARGET_GROUP = PARSER.add_mutually_exclusive_group(required=True)
TARGET_GROUP.add_argument('-g', '--git',
                          help='Process target as an option for git diff',
                          type=str,
                          nargs='?',
                          choices=['STAGED', 'LAST'],
                          const='LAST',
                          action='store',
                          dest='target_type'
)
TARGET_GROUP.add_argument('-f', '--filename',
                          help='Process target as a filename or list of filenames',
                          action='store_const',
                          const='FILE',
                          dest='target_type'
)
TARGET_GROUP.add_argument('-d', '--dirname',
                          help='Process target as a directory or list of directories',
                          action='store_const',
                          const='DIR',
                          dest='target_type'
)

def main():
    # Argument parsing
    ARGS = PARSER.parse_args()
    TARGET      = ARGS.target
    TARGET_TYPE = ARGS.target_type
    VERBOSITY   = (6-ARGS.verbosity)*10
    ###FIXME: excludes Argument
    EXCLUDES = ''
    # Global variable setting
    LOGGER.setLevel(VERBOSITY)
    LOGGER.debug('cmd line args %s', ARGS)
    # Execution
    try:
        EXIT_CODE = pylint_ci.main(TARGET, TARGET_TYPE, EXCLUDES)
    except AssertionError as error:
        LOGGER.critical(error)
        EXIT_CODE = -1
    sys.exit(EXIT_CODE)

if __name__ == '__main__':
    sys.exit(main())
