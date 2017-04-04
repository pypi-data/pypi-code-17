"""Unpack .crx files the way Chrome does."""

from os import path

with open(path.abspath(path.join(path.dirname(__file__), '..', 'VERSION'))) as _v:
    __version__ = _v.read().strip()

del path, _v

from crx_unpack.unpack import *
