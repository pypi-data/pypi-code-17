# repov <https://github.com/msikma/repov>
# Copyright (C) 2015, Michiel Sikma <michiel@sikma.org>
# MIT licensed

from datetime import datetime


def count_hex(string, success):
    '''
    Parser function that modifies the output of the 'count-hex' command.
    This transforms the number into a hexadecimal one. In actuality,
    this is an example of how to use transformer functions for Git output.
    '''
    if success is not True:
        return string

    # Use format() instead of hex() since we don't want the 0x prefix.
    return format(int(string), 'x')


def makedate(string, success):
    '''
    Takes a date returned to us from Git and turns it into a Python date object.
    The date is given in Unix time, e.g. '1486023001'.
    '''
    if success is not True:
        return string
    
    return datetime.fromtimestamp(int(string))


def any_branch(string, success):
    '''
    Parser function that modifies the output of the 'branch-any' command.
    This removes the 'heads/' part from the output for a regular branch.
    '''
    if success is not True:
        return string

    # Filter out heads/ in case of a regular branch name.
    if 'heads/' in string:
        string = string.replace('heads/', '')

    return string


default_args = {
    # Branch name (even while in detached mode).
    'branch': ['for-each-ref --format=\'%(refname:short)\' refs/heads'],
    # Branch name (but returns different answers per mode; see readme).
    'branch-any': ['describe --all', any_branch],
    # All branch names
    'branch-all': ['log -n 1 --pretty=%D HEAD'],
    # Short commit hash.
    'hash': ['rev-parse --short HEAD'],
    # Full commit hash.
    'hash-full': ['rev-parse HEAD'],
    # Revision number (number of commits since initial).
    'count': ['rev-list HEAD --count'],
    # Revision number in hexadecimal (example of how to use a transformer).
    'count-hex': ['rev-list HEAD --count', count_hex],
    # Last commit date
    'last-commit': ['log -n 1 --date=format:%s --pretty=format:%cd', makedate]
}

default_tpl = '%branch-any%-%count%-%hash%'
