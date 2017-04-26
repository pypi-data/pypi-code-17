#!/usr/bin/env python

"""
Tests for the workdir operation
"""

import pathlib
import unittest

import dockerscript.operations

class TestWorkdirOperation(unittest.TestCase):
    """
    Tests for the WorkdirOperation class
    """

    def test_build(self):
        """
        Tests that the operation creates the correct output
        """

        path = pathlib.Path('my_dir')
        operation = dockerscript.operations.WorkdirOperation(path)

        self.assertEqual(
            f'WORKDIR {path}',
            operation.build(),
            'Operation was built correctly',
        )

class TestWorkdir(unittest.TestCase):
    """
    Tests for the workdir function
    """

    def test_string(self):
        """
        Tests that a string path is converted properly
        """

        path = 'my_dir'
        image = dockerscript.Image()

        dockerscript.operations.workdir(image, path)

        self.assertListEqual(
            [
                dockerscript.operations.WorkdirOperation(pathlib.Path(path)),
            ],
            image.operations,
            'Path was converted properly',
        )

    def test_path(self):
        """
        Tests that a path object is used as is
        """

        path = pathlib.Path('my_dir')
        image = dockerscript.Image()

        dockerscript.workdir(image, path)

        self.assertListEqual(
            [
                dockerscript.operations.WorkdirOperation(path),
            ],
            image.operations,
            'Path was used as expected',
        )
