#!/usr/bin/env python

"""
Tests for the Image class
"""

import pathlib
import tempfile
import unittest

import dockerscript.operations

class TestImage(unittest.TestCase):
    """
    Tests for the Image class
    """

    def test_cnstr_filename_str(self):
        """
        Tests that if a filename string is given to the constructor a path is created
        """

        filename = 'my/Dockerfile'

        image = dockerscript.Image(filename=filename)

        self.assertEqual(
            pathlib.Path(filename),
            image.filename,
            'File path was converted correctly',
        )

    def test_cnstr_filename_path(self):
        """
        Tests that if a filename path is given to the constructor it is used as is
        """

        file_path = pathlib.Path('Dockerfile')

        image = dockerscript.Image(filename=file_path)

        self.assertEqual(
            file_path,
            image.filename,
            'File path matched expected',
        )

    def test_add_operation(self):
        """
        Tests that an operation can be added to the image
        """

        operation = dockerscript.operations.BaseImageOperation('test_image')
        image = dockerscript.Image()

        image.add_operation(operation)

        self.assertListEqual(
            [
                operation,
            ],
            image.operations,
            'Image had all the correct operations',
        )

    def test_add_operation_none(self):
        """
        Tests that a null operation cannot be added to the image
        """

        image = dockerscript.Image()

        with self.assertRaises(ValueError):
            image.add_operation(None)

    def test_build_empty(self):
        """
        Tests that nothing happens if no operations were given
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            dockerfile = pathlib.Path(temp_dir, 'Dockerfile')
            image = dockerscript.Image(filename=dockerfile)

            image.build()

            self.assertFalse(
                dockerfile.exists(),
                'File was not created',
            )

    def test_build(self):
        """
        Tests that operations are correctly written out to the requested file
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            dockerfile = pathlib.Path(temp_dir, 'Dockerfile')
            image = dockerscript.Image(filename=dockerfile)

            base_image = 'test_image'
            dockerscript.base_image(image, base_image)

            image.build()

            expected_file = f'FROM {base_image}\n'

            self.assertEqual(
                expected_file,
                dockerfile.read_text(),
                'File contents were written correctly',
            )

    def test_build_exists(self):
        """
        Tests that if the file already exists it is overwritten
        """

        with tempfile.NamedTemporaryFile() as temp_file:
            dockerfile = pathlib.Path(temp_file.name)
            image = dockerscript.Image(filename=dockerfile)

            base_image = 'test_image'
            dockerscript.base_image(image, base_image)

            image.build()

            expected_file = f'FROM {base_image}\n'

            self.assertEqual(
                expected_file,
                dockerfile.read_text(),
                'File contents were written correctly'
            )
