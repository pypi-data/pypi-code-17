#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic Tokens
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


class Token(object):
    type = "Token"

    def __init__(self, token, start=None, end=None):
        self.token = token
        self.start = start
        self.end = end

    def __repr__(self):
        return "{}(token={!r:.50}, start={}, end={})".format(
            self.type, self.token, self.start, self.end)


class Comment(Token):
    type = "Comment"


class Identifier(Token):
    type = "Identifier"


class Keyword(Token):
    type = "Keyword"


class Newline(Token):
    type = "Newline"


class Number(Token):
    type = "Number"


class Operator(Token):
    type = "Operator"


class Punctuation(Token):
    type = "Punctuation"


class String(Token):
    type = "String"


class Whitespace(Token):
    type = "Whitespace"
