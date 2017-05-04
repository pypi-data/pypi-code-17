# -*- coding: utf-8; -*-

# This is part of Oh-My-CAD, a toolkit for distribution, configuration
# and analysis of simple lisp code.

# Copyright (C) 2016 Yuri Teixeira

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

"""Formatting and documentation generation for simple lisp code."""


from configparser import ConfigParser
from collections import OrderedDict
from pathlib import Path

from .parser import parse


def unwrap(text: str):
    '''Return text with unwrapped paragraphs.

    Unwrapped lines of paragraphs are separated by blank lines.
    Leading and trailing whitespaces are removed before unwrapping.
    '''
    text = '\n'.join((line.strip() for line in text.splitlines()))
    paragraphs = text.split('\n\n')
    return '\n\n'.join([' '.join([line for line in paragraph.splitlines()])
                        for paragraph in paragraphs])


def escape_rst(text):
    """Return input string with special characters escaped.

    This is a naive implementation. Works for some characters but is
    not thoroughly implemented.
    """
    return (text
            .replace(r'\\', r'\\\\')
            .replace('*', r'\*')
            .replace('_', r'\_')
            .replace('+', r'\+')
            .replace('-', r'\-')
            # Insert a zero-width-space to prevent joining two hyphens
            # into a dash.
            .replace(r'\-\-', '\\-\u200B\\-'))


def format_lisp(code) -> str:
    """Formatted documentation of the code in reST format."""
    title_fmt = '\n{0:#^{width}}\n{name}\n{0:#^{width}}\n\n'
    heading_fmt = '{0:*^{width}}\n{name}\n{0:*^{width}}\n\n'
    docstring_fmt = '{docstring}\n\n'
    command_fmt = '{name}\n{0:=^{width}}\n\n{docstring}\n\n'
    function_fmt = '(**{name}**{arguments}){nested}\n\n   {docstring}\n\n'
    argument_fmt = '*{a}*'
    global_vars_fmt = '* **{name}** assigned in\n\n{assignments}\n\n'
    assignments_fmt = '   * *{a}*'
    calls_on_load_fmt = '* **{name}**\n'
    output = []
    sections = OrderedDict((('Commands', []),
                            ('Functions', []),
                            ('Global variables', []),
                            ('Functions called on load', [])))
    for function in reversed(code.get('functions', ())):
        name = escape_rst(function['name'])
        docstring = '\n'.join(function['docstring'])
        nested = ''
        arguments = ''
        if function['is_nested']:
            nested = ' nested in *{}*'.format(
                escape_rst(function['ancestor']['name']))
        if function['arguments']:
            arguments = ' ' + ' '.join([argument_fmt.format(a=escape_rst(a))
                                        for a in function['arguments']])
        if function['is_command']:
            name = name[2:]  # Trim 'c:' from command name.
            sections['Commands'].append(
                command_fmt.format('', name=name.upper(),
                                   width=len(name),
                                   docstring=docstring))
        else:
            sections['Functions'].append(
                function_fmt.format(name=name,
                                    arguments=arguments,
                                    nested=nested,
                                    docstring=unwrap(docstring)))
    for name in sorted(code['global_vars']):
        assignments = sorted(set(code['global_vars'][name]['assignments']))
        assignments = [escape_rst(a) for a in assignments]
        assignments = [assignments_fmt.format(a=a) for a in assignments]
        assignments = '\n'.join(assignments)
        sections['Global variables'].append(
            global_vars_fmt.format(name=escape_rst(name),
                                   assignments=assignments))
    for call in reversed(code['calls_on_load']):
        sections['Functions called on load'].append(
            calls_on_load_fmt.format(name=escape_rst(call['first'])))
    title = code['name']
    output.append(title_fmt.format('', name=title, width=len(title)))
    output.append(docstring_fmt.format(docstring='\n'.join(code['docstring'])))
    for heading, body in sections.items():
        if body:
            output.append(heading_fmt.format('', name=heading,
                                             width=len(heading)))
            output.extend(body)
            if body[-1][-2:] != '\n\n':
                output.append('\n')
    return ''.join(output)


def format_conf(path: Path,
                title=None,
                title_fill='*',
                section_fill='=',
                section_formatter=None,
                option_bullet='*',
                option_formatter=None,
                ) -> str:
    """Format configuration file as reST."""
    config = ConfigParser()
    try:
        with path.open() as file:
            config.read_file(file)
    except UnicodeDecodeError:
        with path.open(encoding='windows-1252') as file:
            config.read_file(file)
    if title is None:
        title = path.name
    lines = ['.. -*- coding: utf-8; -*-\n'
             '.. This file was automatically generated\n'
             '.. Modifications may be lost in the next file generation.\n\n'
             '{0:{fill}^{width}}\n{title}\n{0:{fill}^{width}}\n\n'.format(
                 '',
                 title=title,
                 fill=title_fill,
                 width=len(title))]
    for section, options in config.items():
        if (section_formatter is None
                or section_formatter(section, config.default_section) is None):
            if section == config.default_section:
                continue
            section = escape_rst(section)
            lines.append(
                '{section}\n{0:{fill}^{width}}\n\n'.format(
                    '', section=section, fill=section_fill,
                    width=len(section)))
        else:
            lines.append(section_formatter(section, config.default_section))
        for key, value in options.items():
            if (option_formatter is None
                    or option_formatter(section,key, value) is None):
                lines.append('{bullet} {key}: {value}\n'.format(
                    bullet=option_bullet,
                    key=escape_rst(key),
                    value=escape_rst(value)))
            else:
                lines.append(option_formatter(section,key, value))
        if lines[-2:] != '\n\n':
            lines.append('\n')
    return ''.join(lines)


def make_rst(input_files, output_dir: Path, fmt='lisp', verbose=True):
    for path in input_files:
        if not path.is_file():
            continue
        elif fmt == 'lisp':
            formatted = format_lisp(parse(path))
        elif fmt == 'conf':
            formatted = format_conf(path)
        else:
            continue
        if verbose:
            print('Parsed {}'.format(path.name))
        file_path = (output_dir / path.stem).with_suffix('.auto.rst')
        with open(str(file_path), 'w', encoding='utf-8') as file:
            file.write(formatted)


def edit_toctree(index_rst, files):
    with open(str(index_rst), encoding='utf-8') as file:
        index_lines = file.readlines()
    in_toctree = False
    auto_lines = []
    for l, line in enumerate(index_lines):
        if line.strip() == '.. toctree::':
            in_toctree = True
        elif in_toctree:
            if line.strip() == '':
                break
            elif line.strip().endswith('.auto'):
                auto_lines.append(l)
    index_lines = index_lines[:l]
    index_lines.append(' ' * 4  # indentation
                       + path.stem + '.auto\n')
    with open(str(index_rst), 'w', encoding='utf-8') as file:
        file.writelines(index_lines)
