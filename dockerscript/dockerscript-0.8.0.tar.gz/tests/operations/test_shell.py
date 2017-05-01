#!/usr/bin/env python

"""
Tests for the shell operation
"""

import unittest

import dockerscript.operations

class TestShellOperation(unittest.TestCase):
    """
    Tests for the ShellOperation class
    """

    def test_build(self):
        """
        Tests that the build output is correct
        """

        operation = dockerscript.operations.ShellOperation('/bin/zsh', ['-c'])

        self.assertEqual(
            'SHELL ["/bin/zsh", "-c"]',
            operation.build(),
            'Shell was set correctly',
        )

class TestShell(unittest.TestCase):
    """
    Tests for the shell function
    """

    def test_operation_creation(self):
        """
        Tests that the operation is created correctly
        """

        shell = '/bin/zsh'
        arguments = ('-c', )
        image = dockerscript.Image()

        dockerscript.operations.shell(image, shell, *arguments)

        self.assertListEqual(
            [
                dockerscript.operations.ShellOperation(shell, list(arguments)),
            ],
            image.operations,
            'Operation was added correctly',
        )
