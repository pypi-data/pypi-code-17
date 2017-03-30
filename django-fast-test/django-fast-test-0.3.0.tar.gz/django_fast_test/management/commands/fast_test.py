import os
import unittest
from importlib import import_module

from django.conf import settings
from django.core.management.base import BaseCommand


def is_discoverable(label):
    """
    Check if a test label points to a python package or file directory.

    Relative labels like "." and ".." are seen as directories.
    """
    try:
        mod = import_module(label)
    except (ImportError, TypeError):
        pass
    else:
        return hasattr(mod, '__path__')

    return os.path.isdir(os.path.abspath(label))


class Command(BaseCommand):
    help = '''
    快速测试: 没有数据库migration的单元测试, 区别于django test.
    fast_test: unittest that no run db migrations, differently from django test.
    但是连接的不是测试数据库, 而是实际开发用的数据库
    使用django.test.TestCase时每个测试方法后数据库回滚，否则对于数据库的操作会永久保留.
    '''
    test_suite = unittest.TestSuite
    test_runner = unittest.TextTestRunner
    test_loader = unittest.defaultTestLoader
    verbosity = 1
    failfast = False
    default_pattern = 'fast_test*.py'

    def create_parser(self, prog_name, subcommand):
        from argparse import RawTextHelpFormatter
        parser = super(Command, self).create_parser(prog_name, subcommand)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument(
            'test_labels',
            nargs='*',
            help='Module paths to test(测试文件,类或方法);\n'
                 'Can be modulename, modulename.TestCase or modulename.TestCase.test_method\n'
                 'Default all %s files in current project,' % self.default_pattern,
        )
        parser.add_argument(
            '--pattern', '-p',
            dest='pattern',
            type=str,
            default=self.default_pattern,
            help='The test file matching pattern. Defaults to %s.' % self.default_pattern,
        )

    def build_suite(self, test_labels=None, pattern=None):
        suite = self.test_suite()
        test_labels = test_labels or ['.']
        pattern = pattern or self.default_pattern

        for label in test_labels:
            label_as_path = os.path.abspath(label)
            tests = None

            # if a module, or "module.ClassName[.method_name]", just run those
            if not os.path.exists(label_as_path):
                tests = self.test_loader.loadTestsFromName(label)
            elif os.path.isdir(label_as_path):
                tests = self.test_loader.discover(start_dir=label, pattern=pattern, top_level_dir='.')
            else:  # isfile
                rel_path = os.path.relpath(label_as_path, os.path.abspath('.'))
                name = os.path.splitext(rel_path)[0].replace(os.path.sep, '.')
                tests = self.test_loader.loadTestsFromName(name)

            if tests and tests.countTestCases():
                suite.addTests(tests)

        return suite

    def run_suite(self, suite, **kwargs):
        return self.test_runner(
            verbosity=self.verbosity,
            failfast=self.failfast,
        ).run(suite)

    def init(self, *args, **options):
        unittest.installHandler()

    def deinit(self):
        unittest.removeHandler()

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', 1))
        test_labels = options.get('test_labels')
        pattern = options.get('pattern')
        self.init(*args, **options)
        suite = self.build_suite(test_labels, pattern)
        result = self.run_suite(suite)
        self.deinit()
