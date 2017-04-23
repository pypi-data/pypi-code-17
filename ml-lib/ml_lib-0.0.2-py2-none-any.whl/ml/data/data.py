import tensorflow as tf
class Data(object):
    def __init__(self):
        raise NotImplementedError()

    def get_data_iterator(self):
        raise NotImplementedError()

    def get_inputs_dim(self):
        return self.inputs_dim

    def get_labels_dim(self):
        return self.labels_dim

class File_Queue(object):
    def __init__(self, file_list, feature_map, preprocess, inputs_dim, labels_dim, batch_size=100):
        self.file_list = file_list
        self.feature_map = feature_map
        self.preprocess = preprocess
        self.inputs_dim = inputs_dim
        self.labels_dim = labels_dim
        self.batch_size = batch_size

    def start(self):
        file_queue = tf.train.string_input_producer(self.file_list)
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(file_queue)
        features = tf.parse_single_example(serialized_example,
                                           features=self.feature_map)
        single_input, single_label = self.preprocess(features)
        inputs, labels = tf.train.shuffle_batch(
            [single_input, single_label], batch_size=self.batch_size, num_threads=2,
            capacity=1000 + 3 * self.batch_size, min_after_dequeue=1000
        )
        return inputs, labels

    def get_inputs_dim(self):
        return self.inputs_dim

    def get_labels_dim(self):
        return self.labels_dim
