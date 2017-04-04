import numpy
from PIL import Image

from conviz.gradient_ascent_optimizer import GradientAscentOptimizer
from conviz.utils.image_util import ImageUtil


class Visualizer(object):
    """
    A convolutional filter visualizer.
    
    Sample use:
        >>> from keras.models import load_model
        >>> model = load_model("path/to/my/trained/keras/model.h5")
        >>> layer = model.get_layer("my_conv_layer_with_32_filters")
        >>> visualizer = Visualizer(model)
        >>> visualizer.visualize(layer, (8, 4))
    """

    def __init__(self, model):
        """
        Constructs a Visualizer.
        
        :param model: The model to which the visualizer is to be associated.
        """
        self.model = model

    def visualize(self, layer, grid_shape, filter_size=(256, 256),
                  grid_padding=(2, 2), ga_rate=0.5, num_steps=10):
        """
        Visualizes a convolutional layer's filters by generating an image 
        which shows the convolutional filters in a grid.
        
        :param layer: The convolutional layer to visualize.
        :param grid_shape: The shape of the grid as a 2D-tuple.
        :param filter_size: Filter image size in pixels as a 2D-tuple.
        :param grid_padding: Grid padding in pixels as a 2D-tuple.
        :param ga_rate: Gradient ascent rate.
        :param num_steps: Number of gradient ascent steps to perform.
        :return: 
        """
        gao = GradientAscentOptimizer(self.model, ga_rate, num_steps)
        image_score_pairs = self._build_image_score_pairs(gao, layer)
        images, scores = zip(*image_score_pairs)
        imgs = [self._resize_image_array(img, filter_size) for img in images]
        return ImageUtil.build_grid_image(imgs, grid_shape, grid_padding)

    @staticmethod
    def _build_image_score_pairs(gao, layer):
        num_conv_filters = layer.output.shape[3]
        image_score_pairs = []
        for conv_filter_idx in range(num_conv_filters):
            img, score = gao.optimize(layer, conv_filter_idx)
            image_score_pairs.append((img, score))
        return image_score_pairs

    @staticmethod
    def _resize_image_array(img, size):
        return numpy.array(Image.fromarray(img).resize(size, Image.BICUBIC))
