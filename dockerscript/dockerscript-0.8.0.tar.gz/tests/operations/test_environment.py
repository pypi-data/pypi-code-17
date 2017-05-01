#!/usr/bin/env python

"""
Tests for the environment operation
"""

import unittest

import dockerscript.operations

class TestEnvironmentOperation(unittest.TestCase):
    """
    Tests for the EnvironmentOperation class
    """

    def test_build_single(self):
        """
        Tests that operation works for a single key/value pair
        """

        key = 'key'
        value = 'value'
        operation = dockerscript.operations.EnvironmentOperation({key: value})

        self.assertEqual(
            f'ENV {key}={value}',
            operation.build(),
            'Environment variable was properly added',
        )

    def test_build_multiple(self):
        """
        Tests that operation works for multiple key/value pairs
        """

        variables = {
            'key1': 'value1',
            'key2': 'value2',
        }

        operation = dockerscript.operations.EnvironmentOperation(variables)

        self.assertEqual(
            f'ENV key1=value1 \\\n    key2=value2',
            operation.build(),
            'Environment variables were properly added',
        )

class TestEnvironment(unittest.TestCase):
    """
    Tests for the environment function
    """

    def test_dict(self):
        """
        Tests that variables can be given as a dict
        """

        variables = {
            'key1': 'value1',
            'key2': 'value2',
        }

        image = dockerscript.Image()

        dockerscript.operations.environment(image, **variables)

        self.assertListEqual(
            [
                dockerscript.operations.EnvironmentOperation(variables),
            ],
            image.operations,
            'Operation with multiple variables correctly added',
        )

    def test_empty_dict(self):
        """
        Tests that an error is raised when an empty dict is given
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.environment(image)
