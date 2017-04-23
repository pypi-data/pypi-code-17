import unittest
from jenkinscli.cli import run


class TestRun(unittest.TestCase):

    def test_args_parser(self):
        """Simple happy case"""

        args = ["arg1=value", "arg2=value"]
        expected = {
            'arg1': 'value',
            'arg2': 'value'
        }

        got = run.job_arguments_parser(args)
        self.assertEqual(expected, got)

    def test_args_parser_unknown_pattern(self):
        args = ["arg"]
        expected = {}

        got = run.job_arguments_parser(args)
        self.assertEqual(expected, got)