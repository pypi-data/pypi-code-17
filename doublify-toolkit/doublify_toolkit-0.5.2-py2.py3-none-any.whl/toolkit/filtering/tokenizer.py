# The MIT License (MIT)
#
# Copyright (c) 2017 Doublify Technologies
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import re
from enum import Enum
from typing import Iterable

_TOKEN_SPECIFICATION = re.Scanner([
    (r'(["\'])(\\?.)*?\1', lambda _, t: (Token.STRING, t)),
    (r'[0-9]*(\.?[0-9]+)+', lambda _, t: (Token.NUMERIC, t)),
    (r'\w+', lambda _, t: (Token.IDENTIFIER, t)),
    (r'\{|\}', lambda _, t: (Token.PARENTHESES, t)),
    (r'\(|\)', lambda _, t: (Token.CURLY, t)),
    (r'\:', lambda _, t: (Token.COLON, t)),
    (r'[ \t]+', None),
])


class Token(Enum):
    """
    Token type represent.
    """
    STRING = 1

    NUMERIC = 2

    IDENTIFIER = 3

    PARENTHESES = 4

    CURLY = 5

    COLON = 6


def tokenize(query: str) -> Iterable[tuple]:
    """
    :param query: Raw DQL query.
    :return: List tokens.
    :rtype Iterable[tuple]
    """
    reply, _ = _TOKEN_SPECIFICATION.scan(query)
    return reply
