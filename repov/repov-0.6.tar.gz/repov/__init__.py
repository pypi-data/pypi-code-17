# repov <https://github.com/msikma/repov>
# Copyright (C) 2015, Michiel Sikma <michiel@sikma.org>
# MIT licensed

from .parser import Parser
from .defaults import default_args, default_tpl


def get_raw(item):
    '''
    Returns the result of a single item in its raw form.
    This is useful for last-commit which is normally a datetime object.
    '''
    return repov_parser.parse_item(item)


def get_version(tpl=default_tpl):
    '''
    Returns a string with Git repository version information, parsed
    from a passed template string (or the default).
    '''
    segments = repov_parser.parse_segments_from_template(tpl)
    return repov_parser.decorate_template(tpl, segments)

# Reference to the parser instance.
repov_parser = Parser()

# Stick in our default arguments.
repov_parser.merge_git_args(default_args)
