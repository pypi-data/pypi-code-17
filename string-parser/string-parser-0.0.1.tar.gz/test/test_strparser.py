#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""StringParser tests"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import pytest
import regex as re

from strparse import (
    StringParser,
    Token,
    Comment,
    Identifier,
    Keyword,
    Newline,
    Number,
    Operator,
    Whitespace,
)

from strparse.patterns import (
    COMMENT_BLOCK_SLASH_STAR,
    COMMENT_LINE_HASH,
    NEWLINE,
    WHITESPACE,
)

DIDACTIC_LANGUAGE_GRAMMAR = [
    (WHITESPACE, Whitespace),
    (COMMENT_LINE_HASH, Comment),
    (COMMENT_BLOCK_SLASH_STAR, Comment),
    (re.compile(r'(let|foo|bar)'), Keyword),
    (re.compile(r'[a-z_][A-Za-z_]*'), Identifier),
    (re.compile(r'\d+'), Number),
    (re.compile(r'[=+-]'), Operator),
    (NEWLINE, Newline),
    (re.compile('.', re.DOTALL), Token),
]

DIDACTIC_LANGUAGE_SOURCE = ("""# A single-line comment.
 /* block
  * comment
  */
let a = 12
""")


@pytest.fixture
def didactic_parser():
    return StringParser(
        DIDACTIC_LANGUAGE_GRAMMAR,
        DIDACTIC_LANGUAGE_SOURCE,
    )


@pytest.fixture
def didactic_tokens(didactic_parser):
    return [token for token in didactic_parser.tokenize()]


def test_parser():
    assert StringParser([], "")


def test_comment_line(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Comment)]
    assert tokens[0].token == "# A single-line comment.\n"


def test_comment_block(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Comment)]
    assert tokens[1].token == "/* block\n  * comment\n  */"


def test_identifier(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Identifier)]
    assert tokens[0].token == "a"


def test_keyword(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Keyword)]
    assert tokens[0].token == "let"


def test_newline(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Newline)]
    assert len(tokens) > 0


def test_number(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Number)]
    assert tokens[0].token == "12"


def test_operator(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Operator)]
    assert tokens[0].token == "="


def test_whitespace(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if isinstance(token, Whitespace)]
    assert len(tokens) > 0


def test_no_tokens(didactic_tokens):
    tokens = [token
              for token in didactic_tokens
              if type(token) is Token]
    assert len(tokens) == 0


def test_tokenize_exception():
    with pytest.raises(Exception):
        StringParser([('b', Token), ], "aaa").tokenize()
