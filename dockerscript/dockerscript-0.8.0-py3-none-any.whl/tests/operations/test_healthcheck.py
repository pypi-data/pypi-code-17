#!/usr/bin/env python

"""
Tests for the healthcheck operation
"""

import unittest

import dockerscript.operations

class TestHealthcheckOperation(unittest.TestCase):
    """
    Tests for the HealthcheckOperation class
    """

    def test_build_no_options(self):
        """
        Tests that the operation is built even with no options
        """

        operation = dockerscript.operations.HealthcheckOperation(
            'echo "foo"',
        )

        self.assertEqual(
            'HEALTHCHECK  CMD echo "foo"',
            operation.build(),
            'Operation was built correctly with no options',
        )

    def test_build_interval(self):
        """
        Tests that the operation is built with the interval option
        """

        operation = dockerscript.operations.HealthcheckOperation(
            'echo "foo"',
            interval='30s',
        )

        self.assertEqual(
            'HEALTHCHECK --interval=30s CMD echo "foo"',
            operation.build(),
            'Operation was built correctly with interval option',
        )

    def test_build_timeout(self):
        """
        Tests that the operation is built with the timeout option
        """

        operation = dockerscript.operations.HealthcheckOperation(
            'echo "foo"',
            timeout='30s',
        )

        self.assertEqual(
            'HEALTHCHECK --timeout=30s CMD echo "foo"',
            operation.build(),
            'Operation was built correctly with timeout option',
        )

    def test_build_retries(self):
        """
        Tests that the operation is built with the retries option
        """

        operation = dockerscript.operations.HealthcheckOperation(
            'echo "foo"',
            retries=3,
        )

        self.assertEqual(
            'HEALTHCHECK --retries=3 CMD echo "foo"',
            operation.build(),
            'Operation was built correctly with retries option',
        )

    def test_build_all(self):
        """
        Tests that the operation is built with all options
        """

        operation = dockerscript.operations.HealthcheckOperation(
            'echo "foo"',
            interval='5m',
            timeout='30s',
            retries=3,
        )

        self.assertEqual(
            'HEALTHCHECK --interval=5m --timeout=30s --retries=3 CMD echo "foo"',
            operation.build(),
            'Operation was built correctly with all options',
        )

class TestHealthcheck(unittest.TestCase):
    """
    Tests for the healthcheck function
    """

    def test_empty_command_str(self):
        """
        Tests that an empty string is not allowed for the command
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.healthcheck(image, '')

    def test_operation(self):
        """
        Tests that the operation is added correctly
        """

        command = 'echo "foo"'
        interval = '5m'
        timeout = '30s'
        retries = 3
        image = dockerscript.Image()

        dockerscript.operations.healthcheck(
            image,
            command,
            interval=interval,
            timeout=timeout,
            retries=retries,
        )

        self.assertListEqual(
            [
                dockerscript.operations.HealthcheckOperation(
                    command,
                    interval=interval,
                    timeout=timeout,
                    retries=retries,
                ),
            ],
            image.operations,
            'Operation was added to image',
        )
