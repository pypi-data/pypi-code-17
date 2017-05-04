# -*- coding: utf-8; -*-

# This is part of weaklisp, a program for analysis of simple lisp
# code.

# Copyright (C) 2016, 2017 Yuri Teixeira

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.

"""Parser for very simple Lisp code.

Parse code and gather data for analysis and documentation.
"""

from collections import deque, defaultdict, namedtuple
from pathlib import Path

import pyparsing as p


VARIABLE_SETTERS = ('setq', 'alist-set')
FUNCTION_DEFINERS = ('defun',)


Code = namedtuple('Code', ('name', 'parsed', 'nodes', 'docstring', 'functions',
                           'global_vars', 'calls_on_load',))


def parser():
    """Return a pyparsing parser for very simple lisp code."""
    # Windows 1252 characters. Not used. Here for reference only.
    control_characters = '''\
\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\
\u0008\u0009\u000A\u000B\u0000\u000D\u000E\u000F\
\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\
\u0018\u0019\u001A\u001B\u0011\u001D\u001E\u001F\
\u007F\
'''
    numbers = '''\
\u0030\u0031\u0032\u0033\u0034\u0035\u0036\u0037\u0038\u0039'''
    single_quote = '\u0027'
    double_quote = '\u0022'
    parentheses = '\u0028\u0029'
    dot = '\u002E'
    spaces = '\u0020\u00A0'
    # All other Windows 1252 printable characters.
    other_printables = '''\
\u0021\u0023\u0024\u0025\u0026\
\u002A\u002B\u002C\u002D\u002F\
\u003A\u003B\u003C\u003D\u003E\u003F\
\u0040\u0041\u0042\u0043\u0044\u0045\u0046\u0047\
\u0048\u0049\u004A\u004B\u004C\u004D\u004E\u004F\
\u0050\u0051\u0052\u0053\u0054\u0055\u0056\u0057\
\u0058\u0059\u005A\u005B\u005C\u005D\u005E\u005F\
\u0060\u0061\u0062\u0063\u0064\u0065\u0066\u0067\
\u0068\u0069\u006A\u006B\u006C\u006D\u006E\u006F\
\u0070\u0071\u0072\u0073\u0074\u0075\u0076\u0077\
\u0078\u0079\u007A\u007B\u007C\u007D\u007E\
\u20AC\u201A\u0192\u201E\u2026\u2020\u2021\u02C6\
\u2030\u0160\u2039\u0152\u017D\u2018\u2019\u201C\
\u201D\u2022\u2013\u2014\u02DC\u2122\u0161\u203A\
\u0153\u017E\u0178\
\u00A1\u00A2\u00A3\u00A4\u00A5\u00A6\u00A7\
\u00A8\u00A9\u00AA\u00AB\u00AC\u00AD\u00AE\u00AF\
\u00B0\u00B1\u00B2\u00B3\u00B4\u00B5\u00B6\u00B7\
\u00B8\u00B9\u00BA\u00BB\u00BC\u00BD\u00BE\u00BF\
\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5\u00C6\u00C7\
\u00C8\u00C9\u00CA\u00CB\u00CC\u00CD\u00CE\u00CF\
\u00D0\u00D1\u00D2\u00D3\u00D4\u00D5\u00D6\u00D7\
\u00D8\u00D9\u00DA\u00DB\u00DC\u00DD\u00DE\u00DF\
\u00E0\u00E1\u00E2\u00E3\u00E4\u00E5\u00E6\u00E7\
\u00E8\u00E9\u00EA\u00EB\u00EC\u00ED\u00EE\u00EF\
\u00F0\u00F1\u00F2\u00F3\u00F4\u00F5\u00F6\u00F7\
\u00F8\u00F9\u00FA\u00FB\u00FC\u00FD\u00FE\u00FF\
'''
    real = (p.Regex(r'[+-]?\d+\.\d*([eE][+-]?\d+)?') &
            p.NotAny(other_printables)
            ).setParseAction(lambda s, l, t: float(t[0]))
    integer = (p.Word(p.nums) & ~p.NotAny(other_printables)
               ).setParseAction(lambda s, l, t: int(t[0]))
    dot = '.'
    symbol = p.Word(p.nums + dot + other_printables)
    quote = p.Suppress("'")
    quoted_symbol = p.Combine(
        quote + p.Word(p.nums + dot + other_printables))
    double_quoted_string = p.Regex(
        r'"(?:[^"]|(?:"")|(?:\\x[0-9a-fA-F]+)|(?:\\.))*"')
    atom = (dot | real | integer | quoted_symbol | symbol
            | double_quoted_string)
    LPAREN = p.Suppress('(')
    RPAREN = p.Suppress(')')
    sexp = p.Forward()
    list_ = LPAREN + p.Group(p.ZeroOrMore(sexp)) + RPAREN
    quoted_list = quote + LPAREN + p.Group(p.ZeroOrMore(sexp)) + RPAREN
    sexp << (quoted_list | list_ | atom)
    return p.ZeroOrMore(sexp).ignore(';' + p.restOfLine)


def extract_docstring(node):
    """Extract node docstring and put it in its docstring key.

    Modifies the node dict in place.
    """
    if node['parent'] is None:
        start = 0
    elif node['first'] == 'defun':
        start = 3
    else:
        return
    i = 0
    for i, expression in enumerate(node['expressions']):
        if i < start:
            continue
        elif not isinstance(expression, str):
            break
    node['docstring'] = [line.strip('"')
                         for line in node['expressions'][start:i]]


def analyse_function(node):
    """Analyse calls to defun.

    Sets keys name, local_vars to the analysed node and sets key
    nested_functions to the ancestor node. Modifies node dicts in
    place.
    """
    node['name'] = node['expressions'][1]
    node['local_vars'] = node['expressions'][2]
    if '/' in node['local_vars']:
        node['arguments'] = node['local_vars'][:node['local_vars'].index('/')]
    else:
        node['arguments'] = node['local_vars']
    node['is_command'] = node['name'].startswith('c:')
    node['is_nested'] = False
    if node['parent']['parent'] is not None:
        # Function is not top level.
        ancestors = [node['parent']]
        while ancestors[-1]['parent'] is not None:
            ancestors.append(ancestors[-1]['parent'])
        for ancestor in ancestors:
            if ancestor['first'] == 'defun':
                node['is_nested'] = True
                node['ancestor'] = ancestor
                ancestor.setdefault('nested_functions', []).append(node)
                break
        else:  # if not break
            # Weird situation of inner function defined inside a call
            # other than defun.
            pass


def analyse_variable(node):
    """Analyse calls to variable setters.

    Return dict of global variables found.
    """
    global_vars = {}
    if node['first'] == 'setq':
        names = [name for name in node['expressions'][1::2]]
    elif node['first'] == 'alist-set':
        names = [node['expressions'][3]]
    for name in names:
        if node['parent']['parent'] is None:
            var = global_vars.setdefault(name, defaultdict(list))
            var['nodes'].append(node)
            var['assignments'].append('Top level')
        else:
            # The assignment is not top level.
            ancestors = [node['parent']]
            while ancestors[-1]['parent'] is not None:
                ancestors.append(ancestors[-1]['parent'])
            for ancestor in ancestors:
                if ancestor['first'] == 'defun':
                    if (name.casefold() not in
                        [a.casefold() for a in ancestor['local_vars']]):
                        # Global assigned in function.
                        var = global_vars.setdefault(
                            name, defaultdict(list))
                        var['nodes'].append(node)
                        var['assignments'].append(ancestor['name'])
                        break
                    else:
                        # Local in function.
                        break
                elif ((ancestor['first'] == 'foreach'
                       and ancestor['expressions'][1].casefold()
                           == name.casefold())
                      or
                      (ancestor['first'] == 'lambda'
                       and (name.casefold() in
                            [a.casefold() for a in ancestor['expressions'][1]]))):
                    # Local in foreach or lambda.
                    break
            else:  # not break
                # Global variable inside some other call.
                var = global_vars.setdefault(name, defaultdict(list))
                var['nodes'].append(node)
                var['assignments'].append('Call to ' + ancestors[-2]['first'])
    return global_vars


def parse(path: Path):
    """Parse a file of lisp code and return a dict with data about it.

    Calls the appropriate analysis method with each node.
    """
    with path.open(encoding='windows-1252') as file:
        string = file.read()
    parsed = parser().parseString(string, parseAll=True).asList()
    nodes = []
    stack = deque()
    stack.append({'parent': None, 'expressions': parsed})
    while stack:
        current = stack.pop()
        if not any(discovered is current for discovered in nodes):
            nodes.append(current)
            for expression in current['expressions']:
                if (isinstance(expression, list) and len(expression) > 0):
                    stack.append({'parent': current,
                                  'expressions': expression})
    for node in nodes:
        if node['parent'] is None:
            node['first'] = None
        elif isinstance(node['expressions'][0], list):
            node['first'] = 'list'
        else:
            node['first'] = str(node['expressions'][0])
    functions = []
    global_vars = {}
    calls_on_load = []
    for node in nodes:
        extract_docstring(node)
        if node['parent'] is None:
            docstring = node['docstring']
    for node in nodes:
        if node['first'] in FUNCTION_DEFINERS:
            functions.append(node)
            analyse_function(node)
        elif node['first'] in VARIABLE_SETTERS:
            new_vars = analyse_variable(node)
            for name, info in new_vars.items():
                # nodes information can be added here if needed.
                global_var = global_vars.setdefault(name, {'assignments': []})
                global_var['assignments'] += info['assignments']
        elif node['first'] is not None and node['parent']['parent'] is None:
            calls_on_load.append(node)
    return {'name': path.name,
            'parsed': parsed,
            'nodes': nodes,
            'docstring': docstring,
            'functions': functions,
            'global_vars': global_vars,
            'calls_on_load': calls_on_load}
    # return Code(name=path.name,
    #             parsed=parsed,
    #             nodes=nodes,
    #             docstring=docstring,
    #             functions=functions,
    #             global_vars=global_vars,
    #             calls_on_load=calls_on_load)
