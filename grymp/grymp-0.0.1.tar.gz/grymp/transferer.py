# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import shutil
import logging
import six

from grymp import util

logger = logging.getLogger(__name__)


@six.python_2_unicode_compatible
class Transferer(object):
    """
    Oversees the copying and moving of files.
    """

    def __init__(self, confirm_all=False, confirm_overwrite=True,
                 keep_originals=False, dir_mode=0o755):
        """
        Initialise a new transferer instance.

        :param confirm_all: Whether to prompt before all filesystem operations.
        :param confirm_overwrite: Whether to prompt before overwriting files.
        :param keep_originals: Whether to delete copied files.
        :param dir_mode: The mode to use for new directories.
        """
        self._confirm_all = confirm_all
        self._confirm_overwrite = confirm_overwrite
        self._keep_originals = keep_originals
        self._dir_mode = dir_mode

    def _validate(self, dest, message):
        """
        Perform checks prior to a move or copy operation.

        :param dest: The destination file path.
        :param message: The message to use to confirm the operation.
        :return: True if permission is granted; false otherwise.
        """
        # if we've been asked to, get permission to perform the filesystem
        # operation
        if self._confirm_all and not util.question_prompt(message):
            return False

        # if the destination exists and we've been asked to, get permission to
        # overwrite it
        if os.path.exists(dest) and \
                self._confirm_overwrite and \
                not util.question_prompt('Overwrite {0}?'.format(dest)):
            return False

        return True

    def move(self, src, dest):
        """
        Move a file, possibly prompting.

        :param src: The source file path.
        :param dest: The path to move the file to.
        :return: True if the file was moved successfully; False if the user
                 rejected the confirmation.
        :raises OSError: If a filesystem-related error prevented the move.
        """
        if not self._validate(dest, 'Move {0} to {1}?'.format(src, dest)):
            return False

        logger.info('Moving %s to %s', src, dest)
        os.rename(src, dest)
        return True

    def copy_delete(self, src, dest):
        """
        Copy a file, possibly prompting, then possibly delete the original,
        possibly prompting again.

        :param src: The source file path.
        :param dest: The path to copy the file to.
        :return: True if the file was copied successfully; False if the user
                 rejected the copy confirmation. This will be True even if the
                 user decided to reject the delete confirmation.
        :raises OSError: If a filesystem-related error prevented the copy.
        """
        if not self._validate(dest, 'Copy {0} to {1}?'.format(src, dest)):
            return False

        logger.info('Copying %s to %s', src, dest)
        # TODO show progress and make cancelable
        shutil.copy2(src, dest)

        if not self._keep_originals:
            if self._confirm_all and not util.question_prompt(
                        'Delete copied file {0}?'.format(src)):
                return False

            try:
                logger.info('Deleting %s', src)
                os.remove(src)
            except IOError as e:
                # ah well
                util.print_error(
                    'Could not delete file {0}: {1}'.format(src, str(e)))

        return True

    def transfer(self, src, dest):
        """
        Get a file to another place, possibly prompting the user for
        confirmation. If the source and destination are on the same filesystem,
        the file will be moved. Otherwise it will be copied using rsync; in this
        case, the user may also be prompted to delete the original.

        :param src: The path to the source file.
        :param dest: The path to copy or move the file to.
        :return: True if the file was transferred successfully; False if the
                 user cancelled a prompt.
        :raises OSError: If a filesystem-related error occurred.
        """

        logger.debug('Asked to transfer %s to %s', src, dest)

        # Use dirname of dest as the actual dest may not exist so we can't do
        # the same filesystem check
        if util.same_filesystem(src, os.path.dirname(dest)):
            logger.debug('Moving as they are on the same filesystem')
            return self.move(src, dest)

        return self.copy_delete(src, dest)

    def maybe_mkdir(self, path):
        """
        Create a new directory if it does not already exist.

        :param path: The path of the directory.
        :return: True if the directory exists or was created; False if the
                 user cancelled a prompt.
        :raises OSError: If a filesystem-related error occurred.
        """
        if os.path.exists(path):
            os.chmod(path, self._dir_mode)
            return True

        if self._confirm_all and \
                not util.question_prompt('Create directory {0}?'.format(path)):
            return False

        logger.info('Creating directory %s', path)
        os.mkdir(path, self._dir_mode)
        return True

    def __str__(self):
        return 'Transferer(' \
               'confirm_all: {0}, ' \
               'confirm_overwrite: {1}, ' \
               'delete_originals: {2})'.format(
                    self._confirm_all,
                    self._confirm_overwrite,
                    self._keep_originals)
