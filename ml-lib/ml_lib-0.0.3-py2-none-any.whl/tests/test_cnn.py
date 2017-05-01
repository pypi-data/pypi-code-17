from ml.data.mnist import MNIST
from ml.neural_network.layer import ConvLayer, FlatteningLayer, FullyConnectedLayer
from ml.neural_network.neural_network import NeuralNetwork
from ml.neural_network.train import launch_training_task
import tensorflow as tf
import unittest

identity_f = lambda x: x

def cost_f(y, y_hat):
    return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_hat))

gradient_f = tf.train.AdamOptimizer(1e-4).minimize

def accuracy_f(y, y_hat):
    correct_predictions_vector = tf.equal(tf.argmax(y, 1), tf.argmax(y_hat, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predictions_vector, tf.float32))
    return accuracy

def prediction_f(y):
    return tf.argmax(y, 1)

class TestCNN(unittest.TestCase):
    def make_cnn(self, inputs_dim, labels_dim):
        conv_layer_1 = ConvLayer(filter_dim=[4, 4], name='conv_layer_1')
        flattening_layer = FlatteningLayer()
        final_layer = FullyConnectedLayer(name='final_layer', activation_f=identity_f)
        layers = [conv_layer_1, flattening_layer, final_layer]
        layers_dims = [(14, 14, 16), (64,), (10,)]
        network = NeuralNetwork(inputs_dim, labels_dim, layers, layers_dims, cost_f, accuracy_f,
                                gradient_f, prediction_f)
        network.make_computation_graph()
        return network

    def test_cnn(self):
        data = MNIST(dataset='train', flat=False)
        self.make_cnn(data.get_inputs_dim(), data.get_labels_dim())
        iterator = launch_training_task(data, max_iterations=5000)
        train_accuracy = [item['train_accuracy'] for item in iterator]
        information_learned = train_accuracy[-1] - train_accuracy[0]
        self.assertTrue(information_learned > 0.5)
        self.assertTrue(len(train_accuracy) == 6)

if __name__ == '__main__':
    unittest.main()
