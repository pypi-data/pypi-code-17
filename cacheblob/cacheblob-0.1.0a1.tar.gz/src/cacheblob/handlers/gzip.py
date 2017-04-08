# -*- coding: utf-8 -*-

"""
This module implements a gzip handler. It stores item values as gzip files on disk and
uses a SQLite database to store the metadata. This is most convenient if you are using
items as files in another way, or otherwise prefer being able to interact with each item
as a file, and each one is large enough to benefit from compression.
"""

from __future__ import absolute_import

import gzip

from .plaintext import Plaintext

class Gzip(Plaintext):
    """This class implements a handler which stores items as gzip files on disk,
    with a SQLite database used for the indexing.
    """
    def __init__(self, opts=None):
        super(Gzip, self).__init__(opts)

    def _open_helper(self, filename, mode):
        """Open a file with the specified mode. This is split out such that we can handle
        plaintext and gzip files without much source duplication. This is an internal
        utility that is not designed to be called by users.

        :param filename: The filename to be opened.
        :param mode: The file mode to open it under, e.g. 'r' or 'w'.
        """
        return gzip.open(filename, mode)
