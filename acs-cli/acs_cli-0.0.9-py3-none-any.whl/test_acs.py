import unittest
import acscli.acs
import sys


def run(command_line):
    sys.argv = command_line.split()
    acscli.acs.main()


class TestAcs(unittest.TestCase):
    def setUp(self):
        # Ensure the config file exists
        run('acs --profile unit-tests configure')
        run('acs --profile unit-tests login --password admin')

    def test_get_my_details(self):
        # TODO: Need to capture stdout/stderr to do anything useful in these tests.
        # See answer involving contextlib at
        # http://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
        run('acs --profile unit-tests people get-person --person-id=-me-')
