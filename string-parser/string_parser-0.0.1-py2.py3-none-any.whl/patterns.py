#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Common Language Patterns"""

import regex as re

COMMENT_BLOCK_SLASH_STAR = re.compile(
    r'/\*.*?(\*/|\Z)', re.DOTALL | re.MULTILINE)
COMMENT_LINE_HASH = re.compile(r'#.*(\n|\Z)')
COMMENT_LINE_DOUBLE_SLASH = re.compile(r'//.*(\n|\Z)')

NEWLINE = re.compile(r"(\r\n|\n)")
NEWLINE_LF = re.compile(r"\n")
NEWLINE_CRLF = re.compile(r"\r\n")

WHITESPACE = re.compile(r"[ \t\f\v]+")
