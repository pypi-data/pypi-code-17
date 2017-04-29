# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import sys
import logging

import six
from six.moves import input


def print_error(msg):
    """
    Print a string to stderr.

    :param msg: The message to print.
    """
    print(msg, file=sys.stderr)


def decode_cli_arg(arg):
    """
    Turn a bytestring provided by `argparse` into unicode.

    :param arg: The bytestring to decode.
    :return: The argument as a unicode object.
    :raises ValueError: If arg is None.
    """
    if arg is None:
        raise ValueError('Argument cannot be None')

    if sys.version_info.major == 3:
        # already decoded
        return arg

    return arg.decode(sys.getfilesystemencoding())


def log_level_from_vebosity(verbosity):
    """
    Get the `logging` module log level from a verbosity.

    :param verbosity: The number of times the `-v` option was specified.
    :return: The corresponding log level.
    """
    if verbosity == 0:
        return logging.WARNING
    if verbosity == 1:
        return logging.INFO
    return logging.DEBUG


def rchop(string, suffix):
    """
    Remove a suffix from a string if it appears.

    :param string: The string to chip.
    :param suffix: The suffix to remove from the string.
    :return: The string with the suffix removed from the end, if it exists.
    """
    # http://stackoverflow.com/a/3663505
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string


def same_filesystem(*args):
    """
    Ascertain whether a number of paths are all located on the same filesystem.

    :param args: Two or more paths to check; if one argument is passed, the
                 result is True by definition. If a path does not exist, this
                 function will ascend the directory hierarchy to the first one
                 that does exist and compare based on that.
    :return: True if the supplied paths are all on the same filesystem; False
             otherwise.
    """

    def _reduce_until_exists(path):
        """
        Ascend the directory tree from a path until we reach a directory that
        exists.

        :param path: The path to reduce.
        :return: The longest existing prefix of that path, representing a valid
                 directory, or file if unchanged.
        """
        while not os.path.exists(path):
            path = os.path.dirname(path)
        return path

    # inspired by http://stackoverflow.com/a/249796
    return len(set([os.lstat(_reduce_until_exists(path)).st_dev
                    for path in args])) == 1


def question_prompt(question, default=True):
    """
    Ask the user a question and obtain a yes/no answer.

    Default | Input    | Result     | Return
    ========|==========|============|============
    True    | y/ye/yes | True       | True
    True    | n/no     | False      | False
    True    | ''       | None       | True
    True    | blah     | ValueError | <re-prompt>
    True    | C-d      | <N/A>      | True
    --------|----------|------------|------------
    False   | y/ye/yes | True       | True
    False   | n/no     | False      | False
    False   | ''       | None       | False
    False   | blah     | ValueError | <re-prompt>
    False   | C-d      | <N/A>      | False
    --------|----------|------------|------------
    None    | y/ye/yes | True       | True
    None    | n/no     | False      | False
    None    | ''       | None       | <re-prompt>
    None    | blah     | ValueError | <re-prompt>
    None    | C-d      | <N/A>      | EOFError

    :param question: What to ask the user.
    :param default: How to interpret the user's response if they do not enter
                    anything (True/False). 'None' means force the user to make
                    a choice - keep prompting until they do.
    :return: True if the user said yes; false if they said no. Guaranteed not to
             be None.
    :raises ValueError: If an invalid default is passed.
    :raises EOFError: If the user hits C-d and default is None (if default is
                      True/False, that would be returned normally instead).
    """
    _PROMPTS = {
        True: '[Y/n]',
        False: '[y/N]',
        None: '[y/n]'
    }
    _RESPONSES = {
        True: ['y', 'ye', 'yes'],
        False: ['n', 'no'],
        None: ['']
    }

    def _parse_result(response):
        """
        Retrieve the result that corresponds to a response.

        :param response: One of the values in _RESPONSES.
        :return: True, False or None.
        :raises ValueError: If the response is not mapped to a result.
        """
        for result_, responses in six.iteritems(_RESPONSES):
            if response in responses:
                return result_
        raise ValueError('Invalid response received')

    if default not in _PROMPTS.keys():
        raise ValueError('Default prompt result cannot be {0}'.format(default))

    while True:
        print('{0} {1} '.format(question, _PROMPTS[default]), end='')
        try:
            selection = input().lower()
            result = _parse_result(selection)

            if result is None:
                if default is None:
                    # must get an answer
                    print_error('There is no default; please specify y or n')
                    continue

                return default

            return result
        except EOFError:
            # C-d pressed
            if default is None:
                # the user is not expecting None; we can only give them an
                # exception
                raise
            return default
        except ValueError:
            # invalid input that is not empty
            print_error('Please respond with y or n')
            continue
