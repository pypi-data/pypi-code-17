#!/usr/bin/python
# -*- coding: utf-8 -*-

"""PyEmT is a python/emacs tiny syntax checker.

It is a wrapper script which makes it easy to use flymake to run various
syntax checking tools on your code. Since flymake expects to just run
the script with the filename and no other arguments, this file is mainly
expected to be run with only one argument: the target file to check.

It runs the various checkers (currently pylint and pep8) and writes the
results to standard output in a format that the emacs flymake package
can read.

See the
[https://github.com/emin63/pyempt/blob/master/README.md](README.md)
file on github or accompanying this distribution for more details and
how to setup flymake in emacs to use this.

See the [https://github.com/emin63/pyempt/blob/master/LICENSE](LICENSE)
file for the BSD 2-clause simplified license. Basically this is open
source and you can modify freely provided credit is given to the author(s).
"""


import subprocess
import argparse
import sys
import logging
import re

__version__ = '1.0.24'

def make_parser():
    """Make the parser to process the command line.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('target', help='Target file to check.')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--disable', action='append', help=(
        'You can provide as many --disable arguments as you like\n'
        'to disable checkers. For example "--disable pep8" would\n'
        'disable the pep8 checker.'))
    parser.add_argument('--log_level', type=int, help=(
        'Numeric python log level (e.g., %s=%i, %s=%i)\n'
        'for logging' % ('DEBUG', logging.DEBUG, 'INFO', logging.INFO)))

    return parser

def make_kill_regexps():
    """Make dictionary identifying regular expressions to remove from output.

    Some of the checkers provide results that confuse pylint. So we remove
    those.
    """
    result = {
        'pylint_rating' : '^[Yy]our code has been rated.*$'
    }
    return result

def run_checkers(args):
    """Do the work of running the various checkers.
    """
    result = []
    disable = args.disable
    disable = set(disable) if disable else set([])
    pep8_cmd = ['pep8', args.target]
    pylint_cmd = ['pylint', args.target, '-f', 'parseable', '-r', 'n']
    cmd_list = [pep8_cmd, pylint_cmd]
    for my_cmd in cmd_list:
        if my_cmd[0] in disable:
            logging.info('Disabling checker %s', my_cmd[0])
            continue
        my_process = subprocess.Popen(my_cmd, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        output = my_process.stdout.read()
        errs = my_process.stderr.read()
        print(errs.decode('utf8'), file=sys.stderr)
        result.append((my_cmd[0], output.decode('utf8')))

    return result

def prepare_output(results):
    """Cleanup the results and prepare them for output.
    """
    kill_regexps = make_kill_regexps()
    output = []
    for name, data in results:
        for re_name, my_re in kill_regexps.items():
            logging.debug('Cleaning output of %s with re %s', name, re_name)
            output.append(re.sub(my_re, '', data, flags=re.M))
    return output

def main():
    """Run the main program.

    This is the main entry point executed when the script is run.
    """
    parser = make_parser()
    args = parser.parse_args()
    if args.log_level is not None:
        logging.getLogger('').setLevel(args.log_level)
    result = run_checkers(args)
    clean_output = prepare_output(result)
    print('\n'.join(clean_output))

if __name__ == '__main__':
    main()
