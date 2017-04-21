#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
StringParser
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from strscan import StringScanner


class StringParser(object):

    def __init__(self, lexicon, str_):
        self.lexicon = lexicon
        self.scanner = StringScanner(str_)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        while not self.scanner.eos():
            pos = self.scanner.pos
            for pattern, cls in self.lexicon:
                if self.scanner.check(pattern):
                    return cls(
                        self.scanner.scan(pattern),
                        start=self.scanner.prev_pos,
                        end=self.scanner.pos,
                    )

            if self.scanner.pos == pos:
                raise Exception("Cannot tokenize:\n{}".format(
                    self.scanner.rest()))

        raise StopIteration()

    def tokenize(self):
        return [token for token in self]
