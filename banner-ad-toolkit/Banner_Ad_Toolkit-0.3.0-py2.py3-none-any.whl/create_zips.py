# -- coding: utf-8 --

# Copyright 2016 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Create zip files of HTML5 banner ads."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import argparse
import logging
import os
import shutil

# 3rd party
from bashutils import logmsg
from progressbar import ProgressBar
from bashutils.time import secs_to_mins

# App
from adkit.adkit import AdKitBase

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Create zip files of HTML5 banner ads."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_zip_files(self, dirs):
        """Create zip files."""
        logmsg.header('Creating zip files...', self.logger)

        # Create output directory to hold our zips
        output_dir = 'Zips'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        num_zips = 0

        # Create a progress bar
        pbar = ProgressBar(term_width=80, maxval=len(dirs)).start()

        for d in dirs:
            self.logger.debug('Zipping: "%s"' % d)
            parent_dir = os.path.join(os.path.dirname(d).split(os.path.sep)[-1], '')
            if parent_dir == self.input_dir:
                parent_dir = ''
            output_file = os.path.join(output_dir, parent_dir, os.path.basename(d))
            shutil.make_archive(output_file, format="zip", root_dir=d)
            num_zips += 1

            # Update progress bar
            pbar.update(num_zips)

        # Ensure progress bar is finished
        pbar.finish()
        time_elapsed = "(Time Elapsed: {0})".format(secs_to_mins(pbar.seconds_elapsed))

        logmsg.success('Created {0} zip files {1}'.format(num_zips,
                                                          time_elapsed), self.logger)

    def get_parser(self):
        """Return the parsed command line arguments."""
        parser = argparse.ArgumentParser(
            description='Create zip files of HTML5 banner ads.')
        parser.add_argument('-l', '--log', help='Enable logging',
                            action='store_true')
        return parser.parse_args()

    def run(self):
        """Run script."""
        config = self.get_config()
        args = self.get_parser()

        if args.log:
            self.create_logger()

        self.logger.debug('-' * 10)

        self.input_dir = os.path.join(config.get('html5', 'input'), '')

        # Do the stuff we came here to do
        dirs = self.find_ad_dirs()
        self.create_zip_files(dirs)

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
