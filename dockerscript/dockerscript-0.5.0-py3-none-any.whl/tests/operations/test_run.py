#!/usr/bin/env python

"""
Tests for the run operation
"""

import unittest

import dockerscript.operations

class TestRunOperation(unittest.TestCase):
    """
    Tests for the RunOperation class
    """

    def test_single_command(self):
        """
        Tests that the output works correctly for a single command
        """

        command = 'echo "foo"'

        operation = dockerscript.operations.RunOperation([command])

        self.assertEqual(
            f'RUN {command}',
            operation.build(),
            'Single command was formatted correctly',
        )

    def test_multiple_commands(self):
        """
        Tests that the output works correctly for multiple commands
        """

        commands = [
            'echo "foo"',
            'echo "bar"',
        ]

        operation = dockerscript.operations.RunOperation(commands)

        self.assertEqual(
            'RUN set -ex \\\n    && echo "foo" \\\n    && echo "bar"',
            operation.build(),
            'Multiple commands were formatted correctly',
        )

class TestRun(unittest.TestCase):
    """
    Tests for the run function
    """

    def test_single_command(self):
        """
        Tests that a single command can be given
        """

        command = 'echo "foo"'
        image = dockerscript.Image()

        dockerscript.operations.run(image, command)

        self.assertListEqual(
            [
                dockerscript.operations.RunOperation([command]),
            ],
            image.operations,
            'Single command operation was added',
        )

    def test_empty_command(self):
        """
        Tests that an empty string cannot be given
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.run(image, '')

    def test_multiple_commands(self):
        """
        Tests that multiple commands can be given in a single operation
        """

        commands = [
            'echo "foo"',
            'echo "bar"',
        ]

        image = dockerscript.Image()

        dockerscript.operations.run(image, commands)

        self.assertListEqual(
            [
                dockerscript.operations.RunOperation(commands),
            ],
            image.operations,
            'Multiple commands were added',
        )

    def test_empty_list(self):
        """
        Tests that an empty list of commands cannot be given
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.run(image, [])
