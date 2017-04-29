# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import glob
import logging

logger = logging.getLogger(__name__)


class Processor(object):
    """
    Represents a processor that handles a part of a release.
    """

    def __init__(self, fs):
        """
        Initialise a new processor instance.

        :param fs: A Transferer instance to use to execute filesystem
                     operations.
        """
        self._fs = fs

    @staticmethod
    def _find_entry(directory, suffix):
        """
        Find a file or directory with a suffix within a directory.

        :param directory: The directory to search within.
        :param suffix: The file or directory suffix.
        :return: The entry path if found.
        :raises IOError: If there is not exactly 1 matching entry.
        """
        matches = glob.glob('{0}/*{1}'.format(directory, suffix))
        if len(matches) != 1:
            raise IOError(
                'Failed to identify entry ending with {0} in {1}'.format(
                    suffix, directory))
        return matches[0]

    @staticmethod
    def _find_file(directory, extension):
        """
        Find the file with an extension in a directory.

        :param directory: The directory in which to look for the file.
        :param extension: The extension of the file.
        :return: The file path if found.
        :raises IOError: If there is not exactly 1 matching file.
        """
        path = Processor._find_entry(directory, '.' + extension)
        if not os.path.isfile(path):
            raise IOError('Found entry {0} is not a file'.format(path))
        return path
