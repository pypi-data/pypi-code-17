# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Generates an `adkit.ini` file."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import logging
import argparse
import os
import shutil

# 3rd Party
from bashutils import logmsg

# App
from adkit.adkit import AdKitBase

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Generates an `adkit.ini` file."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def copy_files(self):
        """Copy quickstart files from data folder to the CWD."""
        logmsg.header('Copy quickstart files...', self.logger)
        # Loop through all non-hidden files in quickstart directory
        files = [f for f in os.listdir(self.get_data('quickstart')) if not f.startswith('.')]
        for filename in files:
            src = os.path.join(self.get_data('quickstart'), filename)
            dst = os.path.join(os.getcwd(), filename)
            if not os.path.isfile(filename):
                shutil.copy2(src, dst)
                logmsg.info('Copied "{0}"'.format(filename), self.logger)
            else:
                logmsg.warning('"{0}" already exists'.format(filename),
                               self.logger)

    def get_parser(self):
        """Return the parsed command line arguments."""
        parser = argparse.ArgumentParser(
            description='Generates an `adkit.ini` file.')
        parser.add_argument('-l', '--log', help='Enable logging',
                            action='store_true')
        return parser.parse_args()

    def run(self):
        """Run script."""
        # config = self.get_config()
        args = self.get_parser()

        if args.log:
            self.create_logger()

        self.logger.debug('-' * 10)

        # Do the stuff we came here to do
        self.copy_files()

        logmsg.success('DONE!')

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
