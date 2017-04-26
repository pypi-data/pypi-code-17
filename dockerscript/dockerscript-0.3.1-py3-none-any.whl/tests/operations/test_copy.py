#!/usr/bin/env python

"""
Tests for the copy operation
"""

import unittest

import dockerscript.operations

class TestCopyOperation(unittest.TestCase):
    """
    Tests for the CopyOperation class
    """

    def test_single_source(self):
        """
        Tests that a single source file is allowed
        """

        source = 'my_file.txt'
        destination = 'dest'

        operation = dockerscript.operations.CopyOperation(
            [source],
            destination,
        )

        self.assertEqual(
            f'COPY ["{source}", "{destination}"]',
            operation.build(),
            'Output for a single source file was correct',
        )

    def test_multiple_sources(self):
        """
        Tests that multiple source files are allowed
        """

        operation = dockerscript.operations.CopyOperation(
            ['file1', 'file2'],
            'dest',
        )

        self.assertEqual(
            'COPY ["file1", "file2", "dest"]',
            operation.build(),
            'Output for multiple source files was correct',
        )

class TestCopy(unittest.TestCase):
    """
    Tests for the copy function
    """

    def test_no_source(self):
        """
        Tests that we do not allow zero source files
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.copy(image)

    def test_no_destination(self):
        """
        Tests that we do not allow not specifying a destination
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.copy(image, 'file')

    def test_single_source(self):
        """
        Tests that a single source file is allowed
        """

        source = 'file1'
        destination = 'dest'
        image = dockerscript.Image()

        dockerscript.operations.copy(image, source, destination)

        self.assertListEqual(
            [
                dockerscript.operations.CopyOperation([source], destination),
            ],
            image.operations,
            'Copy operation for a single file was added correctly',
        )

    def test_multiple_sources(self):
        """
        Tests that multiple source files are allowed
        """

        sources = ['file1', 'file2']
        destination = 'dest'
        image = dockerscript.Image()

        dockerscript.operations.copy(image, *sources, destination)

        self.assertListEqual(
            [
                dockerscript.operations.CopyOperation(sources, destination),
            ],
            image.operations,
            'Copy operation for multiple source files was added correctly',
        )
