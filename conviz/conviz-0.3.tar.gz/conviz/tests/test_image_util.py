import os
from unittest import TestCase

import numpy
from PIL import Image

from conviz.utils.image_util import ImageUtil


class TestImageUtil(TestCase):
    def setUp(self):
        self.img_save_path = "./test_img.png"
        self._remove_test_image_if_exists()

    def tearDown(self):
        self._remove_test_image_if_exists()

    def test_build_grid_image(self):
        # Create a list of same-size random images
        img_dim = (64, 48, 3)
        images = [numpy.random.random(img_dim) for _ in range(6)]

        # Build a grid image with the list of images
        grid_dim = (3, 2)
        padding = (5, 5)
        grid_img = ImageUtil.build_grid_image(images, grid_dim, padding)

        # Verify that the grid image's dimensions are as expected
        expected_grid_image_shape = (
            padding[0] + (img_dim[0] + padding[0]) * grid_dim[0],
            padding[1] + (img_dim[1] + padding[1]) * grid_dim[1],
            3
        )
        self.assertTupleEqual(
            grid_img.shape[:2],
            expected_grid_image_shape[:2],
            "The build grid image has incorrect shape."
        )

    def test_save_image(self):
        # Define the dimensions of the image data
        img_dim = (128, 256, 3)

        # Create a random array of image data
        img = numpy.random.random(img_dim)

        # Save the image
        ImageUtil.save_image(img, self.img_save_path)

        # Verify that the image file was created
        self.assertTrue(
            os.path.exists(self.img_save_path),
            "Image file was not created when saving image."
        )

        # Load the image from the created file
        loaded_img = Image.open(self.img_save_path)

        # Verify that image dimensions are preserved
        im_size = loaded_img.size
        self.assertTupleEqual(
            (im_size[1], im_size[0]), img_dim[:2],
            "Image dimensions were not preserved when saving image."
        )

        # Verify that image data is preserved
        loaded_img_data = numpy.array(loaded_img) / 255.0
        numpy.testing.assert_array_almost_equal(
            loaded_img_data, img, 2,
            "Data integrity was not preserved when saving image."
        )

    def _remove_test_image_if_exists(self):
        if os.path.exists(self.img_save_path):
            os.remove(self.img_save_path)
