import os
from unittest import TestCase

from conviz.models import cifar10
from conviz.utils.data_util import DataUtil


class TestModels(TestCase):
    def test_cifar10(self):
        # Get the trained CIFAR10 model's path
        model_path = os.path.join(
            DataUtil.get_cache_path(), "models", "cifar10.h5")

        # If the model is already cached, remove it
        if os.path.exists(model_path):
            os.remove(model_path)

        # Load the model (which will be downloaded and cached)
        model = cifar10.load()

        # Verify that the model has been cached
        self.assertTrue(os.path.exists(model_path))

        # Verify that the model minimally works
        model.summary()

        # Remove the cached version of the model
        os.remove(model_path)
