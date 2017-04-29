# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import logging

from grymp import util
from grymp.processors import processor

logger = logging.getLogger(__name__)


class Extras(processor.Processor):
    """
    Handles the processing of release extras.
    """

    _EXTRAS_SUFFIX = 'Extras-Grym'

    @staticmethod
    def _translate_name(name):
        """
        Attempts to resurrect the original file or directory name from the
        Grym/vR version.

        :param name: The mutated name.
        :return: Our best guess at the original name.
        """

        # substrings to remove from any name
        _FRAGMENT_BLACKLIST = ['TrueHD', 'Atmos', 'DD-5.1', '720p', '1080p',
                               'Bluray', 'DTS-HD', 'x264']

        if name.endswith('-Grym'):
            # is directory
            extension = ''
        else:
            # is file
            name, extension = os.path.splitext(name)

        name = util.rchop(name, '-Grym')
        for fragment in _FRAGMENT_BLACKLIST:
            name = name.replace(fragment + '.', '')
        name = name.replace('.', ' ')
        name = name.replace('-', ' - ')
        return name + extension

    def _process_recursive(self, local_dir, remote_dir):
        """
        Recursively transfer extras in a local directory to a remote one.

        :param local_dir: The source directory.
        :param remote_dir: The destination directory.
        :return: True if the transfer finished normally; N.B. not all
                 directories may have been copied. False if the user rejected
                 the creation of a directory - in which case the process cannot
                 continue.
        """
        # we don't use os.walk() as we would have to translate intermediate
        # paths over and over again
        for name in os.listdir(local_dir):
            local_path = os.path.join(local_dir, name)
            translated_name = self._translate_name(name)
            remote_path = os.path.join(remote_dir, translated_name)
            if os.path.isdir(local_path):
                if not self._fs.maybe_mkdir(remote_path) or \
                        not self._process_recursive(local_path, remote_path):
                    # we can't continue if the directory structure isn't there
                    return False
            elif os.path.isfile(local_path):
                self._fs.transfer(local_path, remote_path)
        return True

    def process(self, base, name, extras_dir):
        """
        Process the extras in the release directory.

        :param base: The release directory, containing the feature.
        :param name: The name of the feature.
        :param extras_dir: The directory to move the extras to. A directory will
                           be created within this with the name of the feature.
        :return: True if all extras were transferred successfully; False if the
                 user cancelled a prompt.
        """
        local_dir = self._find_entry(base, self._EXTRAS_SUFFIX)
        logger.debug('Located extras at %s', local_dir)

        remote_dir = os.path.join(extras_dir, name)
        if not self._fs.maybe_mkdir(remote_dir):
            return False

        return self._process_recursive(local_dir, remote_dir)
