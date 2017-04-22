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

import os
import sys
from optparse import OptionParser
from collections import namedtuple

from ._compat import NoSectionError, NoOptionError
from .parser import SchemaConfigParser


__all__ = [
    'configdeck',
    'schemaconfigdeck',
]


SchemaDeck = namedtuple("SchemaDeck",
    "schema_parser option_parser options args")


def schemaconfigdeck(parser, op=None, argv=None):
    """Stacked configuration sources for your application.

    The OptionParser is populated with options and defaults taken from the
    SchemaConfigParser.

    """
    def long_name(option):
        if option.section.name == '__main__':
            return option.name
        return option.section.name + '_' + option.name

    def opt_name(option):
        return long_name(option).replace('-', '_')

    if op is None:
        op = OptionParser()
    if argv is None:
        argv = sys.argv[1:]
    schema = parser.schema

    for section in schema.sections():
        if section.name == '__main__':
            og = op
        else:
            og = op.add_option_group(section.name)
        for option in section.options():
            kwargs = {}
            if option.help:
                kwargs['help'] = option.help
            try:
                kwargs['default'] = parser.get(section.name, option.name)
            except (NoSectionError, NoOptionError):
                pass
            kwargs['action'] = option.action
            args = ['--' + long_name(option)]
            if option.short_name:
                # prepend the option's short name
                args.insert(0, '-' + option.short_name)
            og.add_option(*args, **kwargs)
    options, args = op.parse_args(argv)

    def set_value(section, option, value):
        # if value is not of the right type, cast it
        if not option.validate(value):
            kwargs = {}
            if option.require_parser:
                kwargs['parser'] = parser
            value = option.parse(value, **kwargs)
        parser.set(section.name, option.name, value)

    for section in schema.sections():
        for option in section.options():
            op_value = getattr(options, opt_name(option))
            try:
                parser_value = parser.get(section.name, option.name)
            except (NoSectionError, NoOptionError):
                parser_value = None
            env_value = os.environ.get("CONFIGDECK_{0}".format(
                long_name(option).upper()))

            # 1. op value != parser value
            # 2. op value == parser value != env value
            # 3. op value == parser value == env value or not env value

            # if option is fatal, op_value will be None, so skip this case too
            if op_value != parser_value and not option.fatal:
                set_value(section, option, op_value)
            elif env_value is not None and env_value != parser_value:
                set_value(section, option, env_value)

    return op, options, args


def configdeck(schema_class, configs, op=None, validate=False):
    """Parse configuration files using a provided schema.

    The standard workflow for configdeck is to instantiate a schema class,
    feed it with some config files, and validate the parser state afterwards.
    This utility function executes this standard worfklow so you don't have
    to repeat yourself.

    """
    scp = SchemaConfigParser(schema_class())
    scp.read(configs)
    parser, opts, args = schemaconfigdeck(scp, op=op)
    if validate or getattr(opts, 'validate', False):
        is_valid, reasons = scp.is_valid(report=True)
        if not is_valid:
            parser.error('\n'.join(reasons))
    return SchemaDeck(scp, parser, opts, args)
