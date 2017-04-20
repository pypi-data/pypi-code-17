# -- coding: utf-8 --

# Copyright 2016 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Optimze images for HTML5 banner ads."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
from subprocess import Popen, PIPE
import argparse
import fnmatch
import logging
import os
import pkg_resources
import shlex

# 3rd party
from bashutils import logmsg
from bashutils.time import Timer
from bashutils.time import secs_to_mins
from progressbar import ProgressBar


# App
from adkit.adkit import AdKitBase

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Optimze images for HTML5 banner ads."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_files_matching(self, match='*.png'):
        """Return all files of a type in the input dir no matter how deep."""
        self.logger.info('Get all files matching "%s"' % match)
        # logmsg.info('Get all files matching "%s"' % match, self.logger)
        matches = []
        for root, dirnames, filenames in os.walk(self.input_dir):
            for filename in fnmatch.filter(filenames, match):
                matches.append(os.path.join(root, filename))

        return matches

    def get_size(self, files):
        total_bytes = 0
        for f in files:
            total_bytes += os.path.getsize(f)

        return total_bytes

    def png_crush(self, files):
        """Crush all PNG files provided."""
        logmsg.header('Crushing PNGs...', self.logger)
        num_files = 0
        processed_files = 0

        # create a progress bar
        pbar = ProgressBar(term_width=80, maxval=len(files)).start()

        for f in files:
            if os.path.isfile(f):
                # crush png
                cmd = 'pngquant --quality={0} --skip-if-larger --ext .png --force "{1}"'.format(self.png_quality, f)
                self.logger.debug(cmd)

                proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
                stdout, stderr = proc.communicate()
                status = not bool(proc.returncode)
                if status:
                    processed_files += 1

                # update progress bar
                pbar.update(num_files)
                num_files += 1

        # ensure progress bar is finished
        pbar.finish()
        time_elapsed = "(Time Elapsed: {0})".format(secs_to_mins(pbar.seconds_elapsed))

        result = 'Crushed {0} of {1} files {2}'.format(processed_files,
                                                       len(files),
                                                       time_elapsed)
        logmsg.success(result, self.logger)
        # self.logger.debug(result)

    def image_optim(self, files):
        """Optimize images using ImageOptim GUI. Very time intensive."""
        logmsg.header('Running ImageOptim GUI on all images...', self.logger)
        logmsg.debug('Unable to provide progress for the GUI app. This can take a while...')
        timer = Timer().start()
        # start_time = time.time()

        cmd = '/Applications/ImageOptim.app/Contents/MacOS/ImageOptim %s' % (' '.join(files))
        # print(cmd)

        proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        status = not bool(proc.returncode)
        if status:
            # end_time = time.time()
            # logmsg.success('Time Elapsed: {0}'.format(end_time - start_time))
            logmsg.success('Optimized {0} images (Time Elapsed: {1})'.format(len(files), timer.stop().elapsed()))
        else:
            logmsg.error(stderr.strip())

    def get_parser(self):
        """Return the parsed command line arguments."""
        parser = argparse.ArgumentParser(
            description='Optimize images for HTML5 banner ads.')
        parser.add_argument('-a', '--all', help='All PNG/JPG files',
                            action='store_true')
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

        # Set some vars
        self.input_dir = os.path.join(config.get('html5', 'input'), '')
        self.png_quality = config.get('html5', 'png_quality')

        # Do the stuff we came here to do
        png_files = self.get_files_matching('*.png')

        size_before = self.get_size(png_files)

        self.png_crush(png_files)

        size_after = self.get_size(png_files)

        kb_saved = (size_before - size_after) / 1024
        logmsg.info('%s Kb saved' % kb_saved)

        if args.all:
            jpg_files = self.get_files_matching('*.jpg')
            all_files = jpg_files  ## png_files + jpg_files
            size_before = self.get_size(all_files)
            self.image_optim(all_files)
            size_after = self.get_size(all_files)

            kb_saved = (size_before - size_after) / 1024
            logmsg.info('%s Kb saved' % kb_saved)

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
