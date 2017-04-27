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

        command = 'echo "foo"'
        operation = dockerscript.operations.CommandOperation(command)

        self.assertEqual(
            f'CMD {command}',
            operation.build(),
            'Command was added correctly',
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
