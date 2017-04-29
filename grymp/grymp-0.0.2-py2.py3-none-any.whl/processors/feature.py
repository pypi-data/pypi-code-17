# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import logging

from grymp.processors import processor

logger = logging.getLogger(__name__)


class Feature(processor.Processor):
    """
    Handles the processing of a release's feature.
    """

    # the extension of the feature
    _EXTENSION = 'mkv'

    def process(self, base, name, feature_dir):
        """
        Process the feature in the release directory.

        :param base: The release directory, containing the feature.
        :param name: The name of the feature.
        :param feature_dir: The directory to move the feature to.
        :return: True if the feature was transferred successfully; False if the
                 user cancelled a prompt.
        """
        path = self._find_entry(base, self._EXTENSION)
        logger.debug('Located feature at %s', path)
        return self._fs.transfer(
            path, os.path.join(feature_dir, name + '.' + self._EXTENSION))
