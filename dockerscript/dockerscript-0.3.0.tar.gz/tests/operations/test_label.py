#!/usr/bin/env python

"""
Tests for the label operation
"""

import unittest

import dockerscript.operations

class TestLabelOperation(unittest.TestCase):
    """
    Tests for the LabelOperation class
    """

    def test_build_single(self):
        """
        Tests that bulid works for a single label datum
        """

        operation = dockerscript.operations.LabelOperation(
            {
                'name': 'value',
            },
        )

        self.assertEqual(
            'LABEL "name"="value"',
            operation.build(),
            'Operation for single value was built correctly',
        )

    def test_build_multiple(self):
        """
        Tests that build works for multiple label data
        """

        operation = dockerscript.operations.LabelOperation(
            {
                'key1': 'value1',
                'key2': 'value2',
            },
        )

        self.assertEqual(
            'LABEL "key1"="value1" \\\n      "key2"="value2"',
            operation.build(),
            'Operation for multiple values was built correctly',
        )

class TestLabel(unittest.TestCase):
    """
    Tests for the label function
    """

    def test_key_value(self):
        """
        Tests that if a key value pair are given they are converted properly
        """

        key = 'key'
        value = 'value'

        image = dockerscript.Image()

        dockerscript.operations.label(image, key, value)

        self.assertListEqual(
            [
                dockerscript.operations.LabelOperation({key: value}),
            ],
            image.operations,
            'Operation was correctly added with single key/value pair',
        )

    def test_key_no_value(self):
        """
        Tests that a string key and a value must be given
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.label(image, 'key')

    def test_key_dict(self):
        """
        Tests that when given a dict it is used
        """

        labels = {
            'key1': 'value1',
            'key2': 'value2',
        }

        image = dockerscript.Image()

        dockerscript.operations.label(image, labels)

        self.assertListEqual(
            [
                dockerscript.operations.LabelOperation(labels),
            ],
            image.operations,
            'Operation was correctly added for dict of labels',
        )

    def test_key_empty_dict(self):
        """
        Tests that we don't allow an empty dict
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.label(image, {})
