# -*- coding: utf-8 -*-

import schema
from docopt import docopt, DocoptExit


def parse_args(cmd, doc, args, validator, **kwargs):
    argv = args if cmd is None else [cmd] + args
    args = docopt(doc, argv=argv, **kwargs)
    for item in ('--', '--help', cmd):
        args.pop(item, None)
    try:
        return schema.Schema(validator).validate(args)
    except schema.SchemaError as e:
        raise DocoptExit('{}\n'.format(e))
