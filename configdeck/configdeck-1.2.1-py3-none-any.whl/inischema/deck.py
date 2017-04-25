# -*- coding: utf-8 -*-
###############################################################################
#
# configdeck -- Stacked configuration sources for your application.
#
# A library for simple, DRY configuration of applications
#
# Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
# Copyright © 2009–2013 Canonical Ltd.
#
# This is free software; see the file ‘COPYING’ for details.
#
###############################################################################

"""configdeck lives here
"""

from __future__ import absolute_import

from collections import namedtuple

from configdeck._compat import builtins
from configdeck.deck import schemaconfigdeck
from configdeck.inischema import parsers
from configdeck.inischema.attributed import AttributedConfigParser
from configdeck.parser import SchemaConfigParser
from configdeck.schema import (
    BoolOption,
    IntOption,
    ListOption,
    Schema,
    Section,
    StringOption,
    )


__all__ = [
    'configdeck',
    'ini2schema',
    ]


IniDeck = namedtuple("IniDeck", " option_parser options args")


def ini2schema(fd, p=None):
    """
    Turn a fd that refers to a INI-style schema definition into a
    SchemaConfigParser object

    @param fd: file-like object to read the schema from
    @param p: a parser to use. If not set, uses AttributedConfigParser
    """
    if p is None:
        p = AttributedConfigParser()
    p.read_file(fd)
    p.parse_all()

    parser2option = {
        'unicode': StringOption,
        'int': IntOption,
        'bool': BoolOption,
        'lines': ListOption,
        }

    class MySchema(Schema):
        pass

    for section_name in p.sections():
        if section_name == '__main__':
            section = MySchema
        else:
            section = Section(name=section_name)
            setattr(MySchema, section_name, section)
        for option_name in p.options(section_name):
            option = p.get(section_name, option_name)

            parser = option.attrs.pop('parser', 'unicode')
            parser_args = option.attrs.pop('parser.args', '').split()
            parser_fun = getattr(parsers, parser, None)
            if parser_fun is None:
                parser_fun = getattr(builtins, parser, None)
            if parser_fun is None:
                def parser_fun(x):
                    return x

            attrs = {'name': option_name}
            option_short_name = option.attrs.pop('short_name', None)
            if option_short_name is not None:
                attrs['short_name'] = option_short_name
            option_help = option.attrs.pop('help', None)
            if option_help is not None:
                attrs['help'] = option_help
            if not option.is_empty:
                attrs['default'] = parser_fun(option.value, *parser_args)
            option_action = option.attrs.pop('action', None)
            if option_action is not None:
                attrs['action'] = option_action

            klass = parser2option.get(parser, StringOption)
            if parser == 'lines':
                instance = klass(item=StringOption(), **attrs)
            else:
                instance = klass(**attrs)
            setattr(section, option_name, instance)

    return SchemaConfigParser(MySchema())


def configdeck(fileobj, *filenames, **kwargs):
    args = kwargs.pop('args', None)
    parser, opts, args = schemaconfigdeck(ini2schema(fileobj), argv=args)
    return IniDeck(parser, opts, args)
