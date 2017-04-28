from layer import Layer, np
import cPickle as pickle
import warnings
from math import ceil
from random import shuffle

class BereNet():

	IDENTITY = Layer.FUNCTIONS[0]
	LOGISTIC = Layer.FUNCTIONS[1]
	TANH = Layer.FUNCTIONS[2]
	ARCTAN = Layer.FUNCTIONS[3]
	SOFTSIGN = Layer.FUNCTIONS[4]
	RELU = Layer.FUNCTIONS[5]

	def __init__(self, layers, minibatch_size, functions=[LOGISTIC]):
		assert len(layers) >= 2, 'Must have at least 2 layers'
		assert minibatch_size > 0, 'Minibatch size must be greater than 0'
		assert len(functions) > 0, 'Must specify at least one activation function'

		if minibatch_size == 1:
			warnings.warn('Setting minibatch size to 1 will update the weights after every training case')

		if len(functions) == 1:
			functions = functions * len(layers)
			functions[0] = BereNet.IDENTITY
		else:
			assert len(functions) == len(layers), 'Must have a function for every layer'

		self._layers = []
		self._minibatch_size = minibatch_size
		self.verbosity = 'e'

		input_layer = Layer(layers[0], layers[1], minibatch_size, is_input=True, function=functions[0])

		self._layers.append(input_layer)

		for i in range(1, len(layers) - 1):
			layer = Layer(layers[i], layers[i+1], minibatch_size, function=functions[i])
			self._layers.append(layer)

		output_layer = Layer(layers[-2], layers[-1], minibatch_size, is_output=True, function=functions[-1])

		self._layers.append(output_layer)

		self._previous_gradients = []

	def predict(self, X, softmax_output=False, round=None):
		for i in range(0, len(self._layers) - 1):
			X = self._layers[i].forward_pass(X)

		output = self._layers[-1].forward_pass(X)

		if softmax_output:
			Layer.softmax(output)

		if round is not None:
			output = np.around(output, decimals=round)

		return output

	def _back_propogate(self, output, target, learning_rate, momentum, l2_regularizer):
		self._layers[-1].D = ((output - target) * self._layers[-1].Fp).T

		for i in range(len(self._layers) - 2, 0, -1):
			W_nobias = np.delete(self._layers[i].W, self._layers[i].W.shape[0] - 1, axis=0)
			self._layers[i].D = W_nobias.dot(self._layers[i+1].D) * np.delete(self._layers[i].Fp.T, self._layers[i].Fp.T.shape[0] - 1, axis=0)

		self._update_weights(learning_rate, momentum, l2_regularizer)

	def _update_weights(self, eta, momentum, l2_regularizer):
		for i in range(0, len(self._layers) - 1):
			gradient = eta * (self._layers[i+1].D.dot(self._layers[i].Z)).T

			if momentum != 0:
				if len(self._previous_gradients) <= i:
					self._previous_gradients.append(gradient)
				else:
					gradient += momentum * self._previous_gradients[i]
					self._previous_gradients[i] = gradient

			if l2_regularizer != 0:
				l2_regularization = self._layers[i].W * l2_regularizer
				bias_row = l2_regularization.shape[0] - 1
				l2_regularization[bias_row, :] = 0.

				gradient += l2_regularization

			self._layers[i].W -= gradient

			prev_gradient = gradient

	def _mean_squared_error(self, output, target):
		return ((target - output) ** 2) / 2

	def train(self, training_data, training_targets, learning_rate, epochs,
		validation_data=None, validation_targets=None, momentum=0, bold_driver=False,
		annealing_schedule=0, l2_regularizer=0):
		data_divided, targets_divided = self._divide_data(training_data, training_targets)

		num_samples = len(data_divided)

		indices = range(num_samples)

		del self._previous_gradients[:]

		if bold_driver and num_samples > 1:
			warnings.warn('Bold driver is an adaptation technique for the learning rate designed for full-batch learning.\
				It is not recommended to use it for mini-batch learning as it will likely confuse the algorithm,\
				resulting in poor performance')

		prev_mse = None

		if validation_data is not None and validation_targets is not None:
			mse_measure_data_small = validation_data[:100]
			mse_measure_targets_small = validation_targets[:100]
			mse_measure_data = validation_data
			mse_measure_targets = validation_targets
		else:
			mse_measure_data_small = training_data[:100]
			mse_measure_targets_small = training_targets[:100]
			mse_measure_data = training_data
			mse_measure_targets = training_targets

		for i in xrange(epochs):
			if 'e' in self.verbosity: print 'Epoch:', i

			shuffle(indices)

			for index in xrange(num_samples):
				if 'n' in self.verbosity: print 'Minibatch:', index, 'out of', num_samples

				random_index = indices[index]

				output = self.predict(data_divided[random_index])
				self._back_propogate(output, targets_divided[random_index], learning_rate, momentum, l2_regularizer)

			if 'm' in self.verbosity:
				self._update_mse(mse_measure_data_small, mse_measure_targets_small)
				self._m()

			if bold_driver:
				if not 'm' in self.verbosity:
					self._update_mse(mse_measure_data_small, mse_measure_targets_small)

				if prev_mse is None:
					prev_mse = self.mse
				else:
					if self.mse < prev_mse:
						learning_rate *= 1.03
					elif self.mse - prev_mse >= (10 ** -10):
						learning_rate *= 0.5

			if annealing_schedule != 0:
				learning_rate = learning_rate / (1 + i / float(annealing_schedule))

		self._update_mse(mse_measure_data, mse_measure_targets)

		if 'm' in self.verbosity: self._m()

	def _update_mse(self, validation_data, validation_targets):
		prediction = self.predict(validation_data)
		mean_squared_error = self._mean_squared_error(prediction, validation_targets)
		self.mse = np.linalg.norm(mean_squared_error)

	def _divide_data(self, data, targets):
		assert data.shape[0] == targets.shape[0], 'Data and targets must have the same amount of samples'

		num_samples = data.shape[0]

		data_divided = None
		targets_divided = None

		if num_samples > self._minibatch_size:
			amount = int(ceil(float(data.shape[0]) / self._minibatch_size))
			data_divided = np.array_split(data, amount, axis=0)
			targets_divided = np.array_split(targets, amount, axis=0)
		else:
			if num_samples < self._minibatch_size:
				warnings.warn('You have less samples than your minibatch size, this is likely to affect perfomance of your model.')
			elif num_samples == self._minibatch_size:
				warnings.warn('You have the same amount of samples as your minibatch size, this is the same as performing full-batch learning.')
			
			data_divided = [data]
			targets_divided = [targets]

		if 's' in self.verbosity:
			print 'Num. of samples:', data.shape[0]
			print 'Num. of minibatches:', len(data_divided)
			print 'Minibatch size:', self._minibatch_size

			if data_divided[-1].shape[0] != self._minibatch_size:
				print 'Size of last minibatch:', data_divided[-1].shape[0]

		return data_divided, targets_divided

	def save(self, file_name):
		file = open(file_name, 'wb')
		pickle.dump(self, file)
		file.close()

	@staticmethod
	def load(file_name):
		file = open(file_name, 'rb')
		nn = pickle.load(file)
		file.close()

		return nn

	def show_verbosity_legend(self):
		print 'Verbosity Legend:'

		print 'm is to show mean squared error everytime it changes'
		print 's is to show sample metrics'
		print 'e is to show epochs'
		print 'n is to show minibatch number with every epoch'

	def _m(self):
		print 'MSE:', self.mse