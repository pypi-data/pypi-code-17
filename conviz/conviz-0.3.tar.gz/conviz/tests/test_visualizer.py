from unittest import TestCase

from conviz.models import cifar10
from conviz.visualizer import Visualizer


class TestVisualizer(TestCase):
    def test_visualize(self):
        # Load a model trained on the CIFAR10 dataset
        model = cifar10.load()

        # Create a visualizer for the model
        visualizer = Visualizer(model)

        # Get the layer to visualize
        layer = model.get_layer("conv1")

        # Run the visualizer to generate the layer's visualization
        grid_shape = (4, 8)
        padding = (2, 2)
        filter_size = (256, 256)
        img = visualizer.visualize(layer, grid_shape, filter_size, padding)

        # Verify that the generated image's shape is as expected
        self.assertTupleEqual(
            img.shape,
            (
                padding[0] + grid_shape[0] * (padding[0] + filter_size[0]),
                padding[1] + grid_shape[1] * (padding[1] + filter_size[1]),
                3
             ),
            "The generated visualization image has unexpected shape."
        )
