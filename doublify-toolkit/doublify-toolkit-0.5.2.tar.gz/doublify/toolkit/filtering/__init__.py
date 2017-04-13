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
from enum import Enum
from collections import namedtuple

from .tokenizer import tokenize, Token


class Operation(Enum):
    """
    Operation represent
    """
    EQUAL = 1

    OR = 2

    IN = 3


class Filter(object):
    def __init__(self, operation=Operation.EQUAL, bindings=None):
        self.operation = operation

        if bindings is None:
            bindings = []

        self.bindings = bindings


Query = namedtuple('Query', ('named_bindings', ))


def parse_query(query: str) -> Query:
    """
    :param query: Raw DQL query.
    :return: DQL Query.
    :rtype Query
    """
    reply = tokenize(query)

    named_bindings = dict()

    current_binding = Filter()

    current_name = None

    for token, kind in reply:
        if token == Token.STRING:
            current_binding.bindings.append(kind[1:-1])
        elif token == Token.NUMERIC:
            if '.' in kind:
                binding = float(kind)
            else:
                binding = int(kind)

            current_binding.bindings.append(binding)
        elif token == Token.IDENTIFIER:
            if kind in ('true', 'false'):
                current_binding.bindings.append(kind == 'true')
            elif kind in ('is', 'not'):
                current_binding.bindings.append(kind == 'is')
            else:
                current_name = kind
        elif kind == '{':
            current_binding.operation = Operation.OR
        elif kind == '(':
            current_binding.operation = Operation.IN
        elif kind in ('}', ')'):
            named_bindings[current_name] = current_binding

            current_binding = Filter()
            current_name = None

        if current_name and current_binding.operation == Operation.EQUAL and len(
                current_binding.bindings) >= 1:
            named_bindings[current_name] = current_binding

            current_binding = Filter()
            current_name = None

    return Query(named_bindings=named_bindings)
