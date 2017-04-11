# -*- coding: utf-8 -*-

__author__ = """Miguel González"""
__email__ = 'migonzalvar@gmail.com'
__version__ = '0.1.0'

from typing import Type, TypeVar
import zlib


T = TypeVar('T', bound='ZlibColumn')


class ZlibColumn:
    @classmethod
    def from_compressed(cls: Type[T], b: bytes) -> Type[T]:
        data = zlib.decompress(b)
        payload = data.decode('utf-8')
        return cls(payload)

    def __init__(self, payload: str):
        self.payload = payload
        self._compressed = None

    @property
    def compressed(self) -> bytes:
        if not self._compressed:
            data = zlib.compress(self.payload.encode('utf-8'))
            self._compressed = data
        return self._compressed

    def __str__(self):
        return self.payload.__str__()

    def __eq__(self, other):
        if hasattr(other, 'payload'):
            return self.payload == other.payload
        else:
            return self.payload == other


def adapt_zlibcolumn(z: ZlibColumn) -> bytes:
    return z.compressed


def convert_zlibcolumn(b: bytes) -> ZlibColumn:
    return ZlibColumn.from_compressed(b)
