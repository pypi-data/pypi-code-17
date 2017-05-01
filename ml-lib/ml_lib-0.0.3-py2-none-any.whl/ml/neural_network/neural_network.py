import tensorflow as tf

class NeuralNetwork(object):
    def __init__(self, inputs_dim, outputs_dim, layers, layers_dims, cost_f,
                 accuracy_f, gradient_f, prediction_f, input_queue=None):
        self.inputs_dim = inputs_dim
        self.outputs_dim = outputs_dim
        self.layers = layers
        self.layers_dims = layers_dims
        self.cost_f = cost_f
        self.accuracy_f = accuracy_f
        self.gradient_f = gradient_f
        self.prediction_f = prediction_f
        self.input_queue = input_queue

    def make_computation_graph(self):
        if self.input_queue is not None:
            inputs, labels = self.input_queue.start()
            use_queue = True
        else:
            use_queue = False

        with tf.name_scope('inputs') as scope:
            if use_queue:
                self.x = inputs
            else:
                inputs_dim_copy = list(self.inputs_dim)
                inputs_dim_copy.insert(0, None)
                self.x = tf.placeholder(tf.float32, shape=inputs_dim_copy)
        tf.add_to_collection('x', self.x)

        with tf.name_scope('labels') as scope:
            if use_queue:
                self.y_hat = labels
            else:
                outputs_dim_copy = list(self.outputs_dim)
                outputs_dim_copy.insert(0, None)
                self.y_hat = tf.placeholder(tf.float32, shape=outputs_dim_copy)
        tf.add_to_collection('y_hat', self.y_hat)

        n_layers = len(self.layers_dims)
        layers_outputs = [self.x]
        for i in range(n_layers):
            with tf.name_scope(self.layers[i].get_name()) as scope:
                if i == 0:
                    layer_input_dim = self.inputs_dim
                else:
                    layer_input_dim = self.layers_dims[i-1]
                output = self.layers[i].get_output(layers_outputs[-1], layer_input_dim, self.layers_dims[i])
                layers_outputs.append(output)
        self.y = layers_outputs[-1]

        with tf.name_scope('cost_function') as scope:
            self.cost = self.cost_f(self.y, self.y_hat)
        tf.add_to_collection('cost', self.cost)

        with tf.name_scope('gradient_function') as scope:
            self.train_step = self.gradient_f(self.cost)
        tf.add_to_collection('train_step', self.train_step)

        with tf.name_scope('accuracy_function') as scope:
            self.accuracy = self.accuracy_f(self.y, self.y_hat)
        tf.add_to_collection('accuracy', self.accuracy)
        tf.summary.scalar('train_accuracy', self.accuracy)

        with tf.name_scope('prediction_function') as scope:
            self.prediction = self.prediction_f(self.y)
        tf.add_to_collection('prediction', self.prediction)

        self.merged_summaries = tf.summary.merge_all()
        tf.add_to_collection('merged_summaries', self.merged_summaries)
