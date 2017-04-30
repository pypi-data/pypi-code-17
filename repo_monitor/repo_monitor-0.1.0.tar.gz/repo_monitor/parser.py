import argparse
import sys

from .python.parsers import CoverageParser
from .python.parsers import NosetestParser


class Parser(object):
    def __init__(self):
        self.base_parser = argparse.ArgumentParser(
            description='Retrieve information from test runs',
        )
        self.sub_commands = {
            'coverage_py': CoverageParser,
            'nosetest_py': NosetestParser,
        }
        self.base_parser.add_argument(
            'cmd',
            choices=self.sub_commands.keys(),
            help='Command to use')

    def run(self, args=None):
        args = args or sys.argv[1:]
        command = self.base_parser.parse_args(args[:1]).cmd
        self.sub_commands[command]().run(args[1:])


def main():
    parser = Parser()
    parser.run()
