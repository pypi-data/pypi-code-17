import argparse
import sys

from .constants import DEFAULT_FILE
from .utils import modify_yaml_dictionary


class Parser(object):
    def __init__(self):
        self.base_parser = argparse.ArgumentParser(
            description='Update key-value store in yaml file',
        )
        self.base_parser.add_argument(
            '--file',
            default=DEFAULT_FILE,
            help='KPI file')
        self.base_parser.add_argument(
            'kpi',
            help='KPI to update')
        self.base_parser.add_argument(
            'value',
            help='Value to update the KPI')

    def run(self, args=None):
        args = args or sys.argv[1:]
        parsed_args = self.base_parser.parse_args(args)
        with modify_yaml_dictionary(parsed_args.file) as dictionary:
            dictionary[parsed_args.kpi] = parsed_args.value


def main():
    parser = Parser()
    parser.run()
