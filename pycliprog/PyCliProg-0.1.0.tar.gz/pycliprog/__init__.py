"""
Copyright 2017 Gu Zhengxiong <rectigu@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from logging import getLogger, basicConfig, WARNING
from argparse import ArgumentParser as _ArgumentParser
import sys


logger = getLogger(__name__)


class Prog(object):
    """
    A minimal-complete Python command-line program.
    """
    def __init__(self):
        self.parser = self.make_parser()
        self.add_basic_args()
        self.add_logging_args()
        self.add_args()

        self.args = None

    def start(self):
        try:
            self.args = self.parser.parse_args()
        except ArgError as exc:
            logger.error('ArgError: %s', exc)
            raise

        config = {}
        config.update(level=self.get_level())
        config.update(format=self.get_format())
        if self.args.log_file:
            config.update(filename=self.args.log_file)
            if not self.args.append_log:
                config.update(filemode='w')
        basicConfig(**config)
        logger.info('args: %s', self.args)
        logger.info('config: %s', config)

        try:
            self.main()
        except ExitFailure as exc:
            logger.error('ExitFailure: %s', exc)
            code = 1
        except Exception as exc:
            logger.exception('Unhandled Exception: %s', exc)
            code = 1
        else:
            code = 0
        sys.exit(code)

    def main(self):
        """
        User-defined program entry function.

        Parsed arguments are available as ``self.args``.
        """
        print('It works! Pass ``--help`` to view usage.')

    def get_format(self):
        fmt = 'pid: %(process)d: '
        fmt += '%(asctime)s: %(levelname)s: '
        fmt += '%(module)s.%(funcName)s:%(lineno)s: %(message)s'
        return fmt

    def get_level(self):
        return WARNING + (self.args.quiet-self.args.verbose)*10

    def add_args(self):
        """
        Add custom arguments to the parser here.

        The parser can be accessed with ``self.parser``.
        """
        pass

    def add_logging_args(self):
        self.parser.add_argument('-L', '--log-file',
                                 help='Output logs to the file.')
        self.parser.add_argument('-A', '--append-log',
                                 help='Append logs to the file.')

    def add_basic_args(self):
        self.parser.add_argument('-v', '--verbose',
                                 action='count', default=0,
                                 help='Output more logs.')
        self.parser.add_argument('-q', '--quiet',
                                 action='count', default=0,
                                 help='Output less logs.')

    def make_parser(self):
        """
        Create the argument parser.
        """
        parser = ArgumentParser(description=self.__class__.__name__)
        return parser


class ArgumentParser(_ArgumentParser):
    """
    Throwing feature isn't actually required.
    """
    def error(self, message):
        raise ArgError(message)


class ExitFailure(Exception):
    """
    Think it as ``EXIT_FAILURE`` from ``<stdlib.h>``.
    """
    pass


class ArgError(Exception):
    pass
