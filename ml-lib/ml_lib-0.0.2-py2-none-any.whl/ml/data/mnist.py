from data import Data
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

class MNIST(Data):
    def __init__(self, dataset, inputs_per_batch=50, flat=True):
        assert dataset == 'train' or dataset == 'test'
        mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
        if dataset == 'train':
            self.inputs = mnist.train.images
            self.labels = mnist.train.labels
        else:
            self.inputs = mnist.test.images
            self.labels = mnist.test.labels
        self.flat = flat
        if not self.flat:
            self.inputs = np.reshape(self.inputs, [-1, 28, 28, 1])
        self.inputs_dim = self.inputs[0].shape
        self.labels_dim = self.labels[0].shape
        self.inputs_per_batch = inputs_per_batch

    def get_data_iterator(self):
        for i in range(0, self.inputs.shape[0], self.inputs_per_batch):
            yield self.inputs[i:i+self.inputs_per_batch], self.labels[i:i+self.inputs_per_batch]
