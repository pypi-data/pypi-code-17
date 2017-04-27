#!/usr/bin/env python

"""
Tests for the command operation
"""

import unittest

import dockerscript.operations

class TestCommandOperation(unittest.TestCase):
    """
    Tests for the CommandOperation class
    """

    def test_build(self):
        """
        Tests that the command is added to the image correctly
        """

        operation = dockerscript.operations.CommandOperation('echo "foo bar"')

        self.assertEqual(
            'CMD ["echo", "foo bar"]',
            operation.build(),
            'Command was added correctly',
        )

    def test_build_with_shell(self):
        """
        Tests that the use of the shell can be turned on
        """

        operation = dockerscript.operations.CommandOperation(
            'echo "foo bar"',
            use_shell=True,
        )

        self.assertEqual(
            'CMD echo "foo bar"',
            operation.build(),
            'Command used the system shell',
        )

class TestCommand(unittest.TestCase):
    """
    Tests for the command function
    """

    def test_empty_string(self):
        """
        Tests that empty command strings are not allowed
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.command(image, '')

    def test_command(self):
        """
        Tests that a command can be set
        """

        command = 'echo "foo"'
        image = dockerscript.Image()

        dockerscript.operations.command(image, command)

        self.assertListEqual(
            [
                dockerscript.operations.CommandOperation(command),
            ],
            image.operations,
            'Command operation was added',
        )
