import unittest
import acscli.acs
import sys


def run(command_line):
    sys.argv = command_line.split()
    acscli.acs.main()


class TestAcs(unittest.TestCase):
    def test_login(self):
        run('acs login --username admin --password admin')

    def test_get_my_details(self):
        # TODO: Need to capture stdout/stderr to do anything useful in these tests.
        # See answer involving contextlib at
        # http://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
        run('acs people get-person --person-id=-me-')
