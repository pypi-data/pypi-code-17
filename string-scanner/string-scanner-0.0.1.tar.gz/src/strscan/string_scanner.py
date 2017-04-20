#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
StringScanner
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import regex as re


class StringScanner(object):
    def __init__(self, _str):
        self._str = _str
        self.pos = 0
        self.prev_pos = None
        self.last_match = None

    def check(self, pattern):
        self.match(pattern)
        if self.last_match:
            return self.last_match.group(0)

    def check_until(self, pattern):
        self.search(pattern)
        return self._str[self.pos:self.last_match.end(0)]

    def eos(self):
        return self.pos == len(self._str)

    def get_byte(self):
        self.prev_pos = self.pos
        self.pos += 1
        return self._str[self.prev_pos:self.pos]

    def match(self, pattern):
        rexp = re.compile(pattern)
        self.last_match = rexp.match(self._str, self.pos)

    def peek(self, _len):
        return self._str[self.pos:_len]

    def pre_match(self):
        if self.last_match:
            return self._str[0:self.last_match.start(0)]
        return self._str[0:self.pos]

    def post_match(self):
        if self.last_match:
            return self._str[self.last_match.end(0):]
        return self._str[self.pos:]

    def reset(self):
        self.pos = 0
        self.prev_pos = None
        self.last_match = None

    def rest(self):
        return self._str[self.pos:]

    def scan(self, pattern):
        self.match(pattern)
        if self.last_match:
            self.prev_pos = self.pos
            self.pos = self.last_match.end(0)
            return self.last_match.group(0)
        return None

    def scan_until(self, pattern):
        self.search(pattern)
        if self.last_match:
            self.prev_pos = self.pos
            self.pos = self.last_match.end(0)
            return self._str[self.prev_pos:self.pos]
        return None

    def search(self, pattern):
        rexp = re.compile(pattern)
        self.last_match = rexp.search(self._str, self.pos)

    def skip(self, pattern):
        _str = self.scan(pattern)
        return len(_str)

    def skip_until(self, pattern):
        _str = self.scan_until(pattern)
        return len(_str)

    def unscan(self):
        if self.prev_pos is not None:
            self.pos = self.prev_pos
            self.prev_pos = None
