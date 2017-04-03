#!/usr/bin/env python3

import argparse
import logging
import os

import doxycore

APP_NAME = 'doxytex'
APP_VERSION = '0.1'
APP_NAME_FULL = '{name} v{version}'.format(name=APP_NAME, version=APP_VERSION)
APP_DESCRIPTION = 'Recursively build TeX files in a directory using latexmk'

"""Print unless in quiet mode."""
def message(msg):
    if not FLAGS or not FLAGS.quiet:
        print(msg)

"""Show the version information."""
def version():
    print(APP_NAME_FULL)

def main():
    if FLAGS.version:
        version()
        exit(0)

    if FLAGS.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif FLAGS.quiet:
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)

    jobs = doxycore.get_jobs(
        source_dir=FLAGS.source_dir,
        exclude_dirs=FLAGS.exclude_dirs,
        extensions=FLAGS.ext,
    )

    if FLAGS.pretend:
        exit(0)

    builder = doxycore.Builder(
        build_dir=FLAGS.build_dir,
        command=FLAGS.builder,
        #TODO allow setting these on command line so script can work with
        # something other than latexmk
        #default_options=FLAGS.builder_opts,
        #build_dir_opt=FLAGS.build_dir_opt,
        #job_name_opt=FLAGS.job_name_opt,
        log_file=FLAGS.log_file,
    )

    for job in jobs:
        message('Building {}'.format(job.source_file))

        builder.build_job(job)
        builder.install_job(job, FLAGS.dest_dir)

class FullPath(argparse.Action):
    """Expand user ~ and relative paths for argparse."""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    parser_verbosity_group = parser.add_mutually_exclusive_group()
    parser_verbosity_group.add_argument(
        '-v', '--verbose', action='store_true',
        help='Enable verbose mode (more status messages)')
    parser_verbosity_group.add_argument(
        '-q', '--quiet', action='store_true',
        help='Enable quiet mode (no output)')
    parser.add_argument('--version', action='store_true',
        help='Show version information')

    parser.add_argument('-p', '--pretend', action='store_true',
        help='Do not compile anything. Just list compilable files.')
    parser.add_argument('-s', '--source_dir', default='.', action=FullPath,
        help='Root directory in which to search for source files')
    parser.add_argument('-b', '--build_dir', default='/tmp/doxy', action=FullPath,
        help='Directory to build in. Temporary files will be placed here.')
    parser.add_argument('-d', '--dest_dir', default='doxy', action=FullPath,
        help='Directory to which output files will be copied.')
    parser.add_argument('-l', '--log_file', default='/tmp/doxy/latexmk.log', action=FullPath,
        help='File to which latexmk output is logged')
    parser.add_argument('-e', '--ext', default=['tex'],
        help='File extensions to be compiled (e.g. tex)')
    parser.add_argument('-x', '--exclude_dirs', default=['tex'], action='append',
        help='Directories to exclude from search (e.g. tex subdirectory)')

    parser.add_argument('--builder', default='latexmk',
        help='Path to the builder executable (e.g. latexmk)')

    FLAGS, LATEXMK_OPTIONS = parser.parse_known_args()

    main()
