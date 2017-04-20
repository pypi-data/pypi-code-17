# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Uploads HTML5 banner ads."""

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
import shlex
import sys
import webbrowser

# 3rd party
from bashutils import logmsg
from bashutils.time import Timer

# App
from adkit.adkit import AdKitBase

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Uploads HTML5 banner ads."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_rsync_exclude(self):
        """Create rsync exclude params."""
        params = ''
        if self.exclude_list:
            for f in self.exclude_list:
                params += ' --exclude %s' % f
        return params

    def upload(self):
        """Upload HTML5 ads files."""
        logmsg.header('Uploading HTML5 ad files...', self.logger)

        timer = Timer().start()

        exclude = self.create_rsync_exclude()
        cmd = 'rsync -avzhP {exclude} "{from_dir}" {user}@{ip}:{to_dir}'.format(
            exclude=exclude,
            from_dir=self.input_dir,
            user=self.user,
            ip=self.ip,
            to_dir=self.remote_dir)
        self.logger.debug(cmd)
        proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        status = not bool(proc.returncode)
        if status:
            logmsg.success('Uploaded HTML ad files (Time Elapsed: {0})'.format(
                timer.stop().elapsed()), self.logger)
            # logmsg.debug(stdout.strip())

    def get_links(self):
        """Get all links of the files we uploaded."""
        logmsg.header('Generating links', self.logger)
        links = []
        for root, dirnames, filenames in os.walk(self.input_dir):
            for name in fnmatch.filter(filenames, 'index.html'):
                url = '{0}{1}'.format(self.url, os.path.join(root, name))
                links.append(url)
                print(url)

        return links

    def create_list(self, csv):
        """Create list from a comma delimited string."""
        exclude_list = csv.split(',')
        new_list = []
        for f in exclude_list:
            new_list.append(f.strip())
        return new_list

    def get_parser(self):
        """Return the parsed command line arguments."""
        parser = argparse.ArgumentParser(
            description="Upload HTML5 ads and generate preview links."
        )

        parser.add_argument('-l', '--log', help='Enable logging',
                            action='store_true')
        parser.add_argument('-b', '--browser', help='Open links in browser',
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
        self.input_dir = os.path.join(config.get('html5', 'input')).rstrip('/')
        self.user = config.get('upload', 'user')
        self.ip = config.get('upload', 'ip')
        self.remote_dir = config.get('upload', 'remote_dir')
        self.url = config.get('upload', 'url')
        self.exclude_list = self.create_list(config.get('upload', 'exclude_list'))

        # Do the stuff we came here to do
        # Check if the input dir exists
        if not os.path.isdir(self.input_dir):
            logmsg.error('"{0}" does nots exist'.format(self.input_dir))
            sys.exit()

        # Upload preview files
        self.upload()

        # Get links
        links = self.get_links()
        logmsg.success('%s ads uploaded' % len(links), self.logger)

        # Ask question
        if args.browser and logmsg.confirm('Open all ads in browser'):
            for l in links:
                webbrowser.open(l)

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
