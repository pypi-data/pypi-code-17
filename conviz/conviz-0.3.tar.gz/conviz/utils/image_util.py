import numpy
from scipy.misc import imsave


class ImageUtil(object):
    """
    A utility class which provides image manipulation functionality.
    """

    @staticmethod
    def build_grid_image(images, grid_dim, padding):
        """
        Builds a grid image from a list of images.
        :param images: The list of images to place on the grid image.
        :param grid_dim: A 2-element tuple for the grid's shape.
        :param padding: A 2-element tuple for vertical and horizontal padding.
        :return: The built grid image.
        """
        img_2d_shape = images[0].shape[:2]
        grid_img_shape = ImageUtil._compute_grid_image_shape(
            img_2d_shape, grid_dim, padding)
        grid_img = numpy.zeros(grid_img_shape)
        ImageUtil._place_image_on_grid(
            grid_img, images, grid_dim, img_2d_shape, padding)
        return grid_img

    @staticmethod
    def save_image(img_data, img_path):
        """
        Saves the given image data to the specified image file path.
        :param img_data: The image data as a numpy array.
        :param img_path: The path to which the image is created.
        """
        imsave(img_path, img_data)

    @staticmethod
    def _compute_grid_image_shape(img_2d_shape, grid_dim, padding):
        return (
            (img_2d_shape[0] + padding[0]) * grid_dim[0] + padding[0],
            (img_2d_shape[1] + padding[1]) * grid_dim[1] + padding[1],
            3
        )

    @staticmethod
    def _place_image_on_grid(grid_img, images, grid_dim, img_2d_shape, padding):
        for grid_i in range(grid_dim[0]):
            for grid_j in range(grid_dim[1]):
                img = images[grid_i * grid_dim[1] + grid_j]
                i_st, i_end, j_st, j_end = ImageUtil._compute_grid_image_zone(
                    img_2d_shape, padding, grid_i, grid_j)
                grid_img[i_st:i_end, j_st:j_end, :] = img

    @staticmethod
    def _compute_grid_image_zone(img_2d_shape, padding, grid_i, grid_j):
        grid_i_start = padding[0] + (img_2d_shape[0] + padding[0]) * grid_i
        grid_i_end = grid_i_start + img_2d_shape[0]
        grid_j_start = padding[1] + (img_2d_shape[1] + padding[1]) * grid_j
        grid_j_end = grid_j_start + img_2d_shape[1]
        return grid_i_start, grid_i_end, grid_j_start, grid_j_end
