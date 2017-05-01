from ml.data.data import File_Queue
from ml.neural_network.layer import FlatteningLayer, FullyConnectedLayer
from ml.neural_network.neural_network import NeuralNetwork
from ml.neural_network.train import launch_training_task
import tensorflow as tf

def get_records(path):
    with open(path) as f:
        record_list = f.readlines()
    record_list = [record.strip() for record in record_list]
    return record_list

identity_f = lambda x: x

def cost_f(y, y_hat):
    return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_hat))

def accuracy_f(y, y_hat):
    correct_predictions_vector = tf.equal(tf.argmax(y, 1), tf.argmax(y_hat, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predictions_vector, tf.float32))
    return accuracy

gradient_f = tf.train.AdamOptimizer(1e-4).minimize

def prediction_f(y):
    return tf.argmax(y, 1)

def make_preprocess_function(label_to_filter):
    def preprocess(features):
        inp = tf.concat([features['mean_rgb'],  features['mean_audio']], 0)
        labels = tf.sparse_to_indicator(features["labels"], 4716)
        labels.set_shape([4716])
        single_label = labels[label_to_filter]
        single_label = tf.one_hot(indices=tf.cast(single_label, tf.int32), depth=2)
        single_label = tf.cast(single_label, tf.float32)
        return inp, single_label
    return preprocess

def make_conv_network(inputs_dim, labels_dim, input_queue):
    layer_1 = FullyConnectedLayer(name='layer_1', activation_f=tf.nn.relu)
    final_layer = FullyConnectedLayer(name='final_layer', activation_f=identity_f)
    layers = [layer_1, final_layer]
    layers_dims = [(1024,), (2,)]
    network = NeuralNetwork(inputs_dim, labels_dim, layers, layers_dims, cost_f, accuracy_f,
                            gradient_f, prediction_f, input_queue)
    network.make_computation_graph()
    return network

if __name__ == "__main__":
    feature_map = {'labels': tf.VarLenFeature(dtype=tf.int64),
                   'video_id': tf.FixedLenFeature(shape=[], dtype=tf.string, default_value=None),
                   'mean_rgb': tf.FixedLenFeature(shape=[1024], dtype=tf.float32, default_value=None),
                   'mean_audio': tf.FixedLenFeature(shape=[128], dtype=tf.float32, default_value=None)}
    inputs_dim = [1152]
    labels_dim = [2]
    preprocess = make_preprocess_function(0)
    record_list = get_records('./machine-learning/scripts/youtube8m/record_list.txt')
    print(record_list)
    data = File_Queue(record_list, feature_map, preprocess,
                      inputs_dim=inputs_dim, labels_dim=labels_dim, batch_size=1000)
    make_conv_network(inputs_dim, labels_dim, data)
    iterator = launch_training_task(data, use_queue=True)
    while True:
        next(iterator)
