"""Where statement parser."""

from __future__ import absolute_import, division, print_function

from pyparsing import (
    CaselessLiteral, Combine, Forward, Group, Keyword, Optional, Word, ZeroOrMore,
    alphas, alphanums, delimitedList, nums, oneOf, quotedString
)


# Tokens
COLUMN = Word(alphas, alphanums + "_$")

AND = Keyword("and", caseless=True)
OR = Keyword("or", caseless=True)
IN = Keyword("in", caseless=True)
E = CaselessLiteral("E")

OPERATORS = oneOf("= == != < > >= <= eq ne lt le gt ge", caseless=True)
SIGN = Word("+-", exact=1)

REAL = Combine(
    Optional(SIGN) +
    (Word(nums) + "." + Optional(Word(nums)) | ("." + Word(nums))) +
    Optional(E + Optional(SIGN) + Word(nums))
)

INTEGER = Combine(
    Optional(SIGN) +
    Word(nums) +
    Optional(E + Optional("+") + Word(nums))
)

PARAMETER = Keyword('?')

VALUE = REAL | INTEGER | PARAMETER | quotedString | COLUMN

# Parser
WHERE = Forward()

CONDITION = Group(
    (COLUMN + OPERATORS + VALUE) |
    (COLUMN + IN + "(" + delimitedList(VALUE) + ")") |
    ("(" + WHERE + ")")
)

WHERE << CONDITION + ZeroOrMore((AND | OR) + WHERE)
