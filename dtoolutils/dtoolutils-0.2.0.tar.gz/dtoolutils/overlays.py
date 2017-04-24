"""Module with utility functions for creating dataset overlays."""

import os

import puremagic
import binaryornot.check


def _categorise_binary(fpath):
    info = puremagic.magic_file(fpath)
    mimetype = None
    for item in info:
        guess = item[1]
        if guess != u"":
            mimetype = guess
    return mimetype


def _categorise_plaintext(fpath):
    size = os.stat(fpath).st_size
    if size == 0:
        return u"inode/x-empty"
    return u"text/plain"


def _mimetype(fpath):
    if binaryornot.check.is_binary(fpath):
        mimetype = _categorise_binary(fpath)
        if mimetype:
            return mimetype
        return u"application/octet-stream"
    return _categorise_plaintext(fpath)


def add_mimetype(dataset):
    """Add a mimetype overlay to the dataset.

    :param dataset: :class:`dtoolcore.DataSet`
    """
    mimetype_overlay = dataset.empty_overlay()
    for i in dataset.identifiers:
        fpath = dataset.abspath_from_identifier(i)
        mimetype_overlay[i] = _mimetype(fpath)
    dataset.persist_overlay("mimetype", mimetype_overlay, overwrite=True)
