#!/usr/bin/env python

"""
Tests for the expose operation
"""

import unittest

import dockerscript.operations

class TestExposeOperation(unittest.TestCase):
    """
    Tests for the ExposeOperation class
    """

    def test_single_port(self):
        """
        Tests that a single port is allowed
        """

        operation = dockerscript.operations.ExposeOperation([22])

        self.assertEqual(
            'EXPOSE 22',
            operation.build(),
            'Single port was exposed',
        )

    def test_multiple_ports(self):
        """
        Tests that multiple ports can be exposed
        """

        operation = dockerscript.operations.ExposeOperation([22, 80])

        self.assertEqual(
            'EXPOSE 22 80',
            operation.build(),
            'Multiple ports were exposed',
        )

    def test_range(self):
        """
        Tests that port ranges are allowed
        """

        operation = dockerscript.operations.ExposeOperation([22, '1000-1200'])

        self.assertEqual(
            'EXPOSE 22 1000-1200',
            operation.build(),
            'Port range was exposed',
        )

class TestExpose(unittest.TestCase):
    """
    Tests for the expose function
    """

    def test_empty_set(self):
        """
        Tests that an empty set of ports is not allowed
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.expose(image)

    def test_ports(self):
        """
        Tests that ports are passed on to the operation
        """

        ports = [22, '8000-8080']
        image = dockerscript.Image()

        dockerscript.operations.expose(image, *ports)

        self.assertListEqual(
            [
                dockerscript.operations.ExposeOperation(ports),
            ],
            image.operations,
            'Expose operation was added to the image',
        )
