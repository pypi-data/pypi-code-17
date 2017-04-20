# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Generates HTML to preview SWF and static banner ads."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
from subprocess import Popen, PIPE
import argparse
import logging
import os
import pkg_resources
import re
import shlex
import shutil

# 3rd party
from bashutils import logmsg
from bashutils.time import Timer
import six
import six.moves.configparser as configparser

# App
from adkit.adkit import AdKitBase

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Generates HTML to preview SWF and static banner ads."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def copy_files(self):
        """Copy files."""
        dest = os.path.join(self.input_dir, 'js')

        if not os.path.isdir(dest):
            if self.verbose:
                logmsg.info('Creating "js" directory...')
            shutil.copytree(self.get_data('js'), dest)
        else:
            if self.verbose:
                logmsg.warning('"js" directory already exists')

    @staticmethod
    def replace_all(text, dict):
        """Replace all."""
        for src, target in six.iteritems(dict):
            text = text.replace(src, target)
        return text

    def create_html(self, filename):
        """
        Create a HTML file for a specific swf/jpg.

        :param str size: width x height (eg - 300x250)
        :param str name: output file name
        :rtype bool:
        """
        # get filename and extension
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]

        # get size
        size = self.get_size_from_filename(name)

        # get width height based on size string (eg - 300x250)
        width, height = size.split('x')

        # open the template and open a new file for writing
        html = pkg_resources.resource_string(__name__, 'templates/template.html').decode("utf-8")
        #print(html)
        outfile = open(filename, 'w')

        # replace the variables with the correct value
        replacements = {
            '{{filename}}': name,
            '{{size}}': size,
            '{{width}}': width,
            '{{height}}': height,
        }

        html = Main.replace_all(html, replacements)
        outfile.write(html)
        outfile.close()

    def generate_html(self):
        """
        Loop through all files in the input directory and create an HTML preview
        page for the swf and static version.
        """
        num_files = 0

        # Loop through all SWF files in the input directory
        files = [f for f in os.listdir(self.input_dir) if f.endswith('.swf')]
        for filen in files:
            filepath = os.path.join(self.input_dir, filen)
            if os.path.isfile(filepath):
                # get filename and extension
                basename = os.path.basename(filepath)
                name = os.path.splitext(basename)[0]

                # create a filename
                filename = os.path.join(self.input_dir, name+'.html')

                # do not overwrite existing HTML files (that would be bad)
                if os.path.isfile(filename):
                    if self.verbose:
                        basen = os.path.basename(filename)
                        logmsg.warning('"{0}" already exists'.format(basen))
                    continue

                self.create_html(filename)
                num_files += 1

        logmsg.success('Generated {0} HTML files'.format(num_files))

    def get_parser(self):
        """Return the parsed command line arguments."""
        parser = argparse.ArgumentParser(
            description='Generate CSS for HTML5 banners..')
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

        self.input_dir = config.get('html5', 'input')

        # Check if the input dir exists
        if not os.path.isdir(self.input_dir):
            logmsg.error('"{0}" does not exist'.format(self.input_dir))
            sys.exit()

        # Do the stuff we came here to do
        timer = Timer().start()


        logmsg.success('HTML Generated (Elapsed time: %s)' % timer.stop().elapsed())


# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
