# -- coding: utf-8 --

# Copyright 2016 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Generates CSS for HTML5 banner ads."""

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
import shlex

# 3rd party
from bashutils import logmsg
from bashutils.time import Timer
from PIL import Image
import cssutils
import six

# App
from adkit.adkit import AdKitBase

# Set global cssutils prefs
cssutils.ser.prefs.indentClosingBrace = False
cssutils.ser.prefs.omitLastSemicolon = False

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Generates CSS for HTML5 banner ads.."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_image_files(self, dirpath, exts=['.png', '.jpg', '.gif']):
        """Get the files we're interested in."""
        files = []
        for f in os.listdir(dirpath):
            # get filename and extension
            basename = os.path.basename(f)
            name, ext = os.path.splitext(basename)
            if basename not in self.ignore_list:
                if ext in exts:
                    files.append(f)
            else:
                self.logger.debug('Ignoring file: %s' % basename)

        return files

    def get_image_info(self, filepath):
        """Return file info."""
        # Get filename and extension
        basename = os.path.basename(filepath)
        name = os.path.splitext(basename)[0]

        # Open and determine image dimensions
        with Image.open(filepath) as im:
            width, height = im.size

        return dict(basename=basename, name=name, width=width, height=height)

    def replace_all(self, text, dict):
        """Replace all."""
        for src, target in six.iteritems(dict):
            text = text.replace(src, target)
        return text

    def create_base_css(self, dirpath, css_file):
        """
        Create the base style.css based on our template.
        """
        # get size
        size = self.get_size_from_filename(dirpath)

        # get width height based on size string (eg - 300x250)
        width, height = size.split('x')

        # open the template and open a new file for writing
        html = pkg_resources.resource_string(__name__, 'templates/style.css').decode('utf-8')
        outfile = open(css_file, 'w')

        # replace the variables with the correct value
        replacements = {
            '{{width}}': str(int(width) - 2),
            '{{height}}': str(int(height) - 2),
        }

        html = self.replace_all(html, replacements)
        outfile.write(html)
        outfile.close()

    def generate_css(self, dirpath):
        """
        Loop through all files in the input directory and
        create CSS styles for them.
        """
        logmsg.header('Create CSS for ad "%s"' % os.path.basename(dirpath))

        css = ''
        num_styles = 0

        # ----------
        # Try to parse existing CSS file
        images_dir = os.path.join(dirpath, self.images_dir)
        files = self.get_image_files(images_dir)

        css_dir = os.path.join(dirpath, self.style_dir)
        css_file = os.path.join(css_dir, 'style.css')
        if os.path.isfile(css_file):
            css_parser = cssutils.parseFile(css_file)

            # CSS file exists, update it
            # logmsg.info('CSS file exists, update it')

            # Loop through all rules
            for rule in css_parser.cssRules:
                if isinstance(rule, cssutils.css.CSSCharsetRule):
                    css += rule.cssText + '\n'
                if isinstance(rule, cssutils.css.CSSComment):
                    css += rule.cssText + '\n'
                if isinstance(rule, cssutils.css.CSSStyleRule):
                    # If one of our images is used in the style, update it
                    for filen in files:
                        filepath = os.path.join(images_dir, filen)
                        img = self.get_image_info(filepath)

                        if img['basename'] in rule.style.background:
                            files.remove(filen)
                            # print('Updating style: %s' % rule.selectorText)
                            rule.style.width = '%dpx' % img['width']
                            rule.style.height = '%dpx' % img['height']
                            num_styles += 1

                    css += rule.cssText + '\n\n'
                    # num_styles += 1

            # Write CSS to file
            # css_file = os.path.join(css_dir, 'style_new.css')
            with open(css_file, 'w') as tf:
                tf.write(css)

            logmsg.success('Updated {0} CSS styles'.format(num_styles))
            return

        # ----------
        # CSS file does not exists, create it
        # logmsg.info('CSS file does not exist, create it')

        self.create_base_css(dirpath, css_file)

        # Loop through all image files in the input directory
        for filen in files:
            filepath = os.path.join(images_dir, filen)
            img = self.get_image_info(filepath)

            # Create a new rule
            rule = cssutils.css.CSSStyleRule()
            rule.selectorText = '#%s' % img['name']
            rule.style.background = 'url(%s) no-repeat' % img['basename']
            rule.style.width = '%dpx' % img['width']
            rule.style.height = '%dpx' % img['height']
            rule.style.position = 'absolute'
            rule.style.top = '0px'
            rule.style.left = '0px'
            if 'bg' not in img['basename']:
                rule.style.zIndex = '100'
            # print(rule.cssText)

            css += rule.cssText + '\n\n'

            num_styles += 1

        # Write CSS to file
        # css_file = os.path.join(css_dir, 'style_new.css')
        with open(css_file, 'a') as tf:
            tf.write(css)

        logmsg.success('Generated {0} CSS styles'.format(num_styles))

    def trim_pngs(self, dirpath):
        """Trim all PNG files of any extra transparency."""
        logmsg.header('Trim PNGs...', self.logger)

        images_dir = os.path.join(dirpath, self.images_dir)
        files = self.get_image_files(images_dir, ['.png'])
        for f in files:
            filepath = os.path.join(images_dir, f)
            self.trim_png(filepath)

    def trim_png(self, filepath):
        """Trim PNG image of only its extra transparency."""
        # We add a border of none to ensure we only remove transparency
        cmd = 'convert -bordercolor none -border 1x1 {0} -trim {0}'.format(filepath)
        self.logger.debug(cmd)

        proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        status = not bool(proc.returncode)
        # if status:
        #     print('yay')

    def create_list(self, csv):
        """Create list from a comma delimited string."""
        current_list = csv.split(',')
        new_list = []
        for f in current_list:
            new_list.append(f.strip())
        return new_list

    def get_parser(self):
        """Return the parsed command line arguments."""
        parser = argparse.ArgumentParser(
            description='Generate CSS for HTML5 banners.')
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
        self.images_dir = config.get('css', 'images_dir')
        self.style_dir = config.get('css', 'style_dir')
        self.ignore_list = self.create_list(config.get('css', 'exclude_list'))

        # Do the stuff we came here to do
        timer = Timer().start()
        dirs = self.find_ad_dirs()

        for d in dirs:
            # TODO: Trim needs work...screws up our pngs
            # self.trim_pngs(d)
            self.generate_css(d)

        logmsg.success('CSS Generated (Elapsed time: %s)' % timer.stop().elapsed())

# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
