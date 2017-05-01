"""
Tests for the base_image operation
"""

import unittest

import dockerscript.operations

class TestBaseImageOperation(unittest.TestCase):
    """
    Tests for the BaseImageOperation class
    """

    def test_build_only_name(self):
        """
        Tests the output of build with only name
        """

        operation = dockerscript.operations.BaseImageOperation(
            'test_image',
        )

        self.assertEqual(
            'FROM test_image',
            operation.build(),
            'Operation with name only matched',
        )

    def test_build_with_tag(self):
        """
        Tests the output of build with a name and a tag
        """

        operation = dockerscript.operations.BaseImageOperation(
            'test_image',
            tag='latest',
        )

        self.assertEqual(
            'FROM test_image:latest',
            operation.build(),
            'Operation with name and tag matched',
        )

    def test_build_with_digest(self):
        """
        Tests the output of build with a name and a digest
        """

        operation = dockerscript.operations.BaseImageOperation(
            'test_image',
            digest='deadbeef',
        )

        self.assertEqual(
            'FROM test_image@deadbeef',
            operation.build(),
            'Operation with name and digest matched',
        )

class TestBaseImage(unittest.TestCase):
    """
    Tests for the base_image operation
    """

    def test_with_name(self):
        """
        Tests that an operation is created and added with only a name
        """

        name = 'test_image'
        image = dockerscript.Image()

        dockerscript.operations.base_image(image, name)

        self.assertListEqual(
            [
                dockerscript.operations.BaseImageOperation(
                    name=name,
                ),
            ],
            image.operations,
            'List of operations included base_image with name',
        )

    def test_with_tag(self):
        """
        Tests that an operation is created and added with a name and tag
        """

        name = 'test_image'
        tag = 'latest'
        image = dockerscript.Image()

        dockerscript.operations.base_image(image, name, tag=tag)

        self.assertListEqual(
            [
                dockerscript.operations.BaseImageOperation(
                    name=name,
                    tag=tag,
                ),
            ],
            image.operations,
            'List of operations included base_iamge with name and tag',
        )

    def test_with_digest(self):
        """
        Tests that an operation is created and added with a name and digest
        """

        name = 'test_image'
        digest = 'deadbeef'
        image = dockerscript.Image()

        dockerscript.operations.base_image(image, name, digest=digest)

        self.assertListEqual(
            [
                dockerscript.operations.BaseImageOperation(
                    name=name,
                    digest=digest,
                ),
            ],
            image.operations,
            'List of operations included base_image with name and digest',
        )

    def test_with_tag_and_digest(self):
        """
        Tests that the function fails if a tag and a digest are given
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            dockerscript.operations.base_image(
                image,
                'test_image',
                tag='latest',
                digest='deadbeef',
            )
