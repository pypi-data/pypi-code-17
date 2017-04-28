import numpy as np

class Layer(object):

	FUNCTIONS = (		# range of functions
		'identity',		# (-inf, inf)
		'logistic',		# [0, 1]
		'tanh',			# (-1, 1)
		'arctan',		# (-pi/2, pi/2)
		'softsign',		# (-1, 1)
		'relu',			# [0, inf)
	)

	def __init__(self, inputs, outputs, minibatch_size, is_input=False, is_output=False, function=FUNCTIONS[0]):
		assert not (is_input and is_output), 'Layer cannot be an input and output layer'

		self.S = np.zeros((minibatch_size, inputs + 1))
		self.Z = np.zeros((minibatch_size, inputs + 1))
		self.Fp = np.zeros((minibatch_size, inputs + 1))
		self.W = None
		self.D = None

		if not is_output:
			self.W = np.random.normal(size=(inputs + 1, outputs), scale=1E-4)
		
		if not is_input:
			if is_output:
				self.D = np.zeros((outputs, minibatch_size))
			else:
				self.D = self.S.T

		self._function = function
		self._is_input = is_input
		self._is_output = is_output

	def forward_pass(self, X):
		if not self._is_output:
			self.S = np.append(X, np.ones((X.shape[0], 1)), axis=1)
		else:
			self.S = X

		self.Z, self.Fp = self._activate(self.S)

		if self._is_output:
			return self.Z
		else:
			return self.Z.dot(self.W)

	def _activate(self, X):
		if self._function == self.FUNCTIONS[0]:
			return self._identity(X)
		elif self._function == self.FUNCTIONS[1]:
			return self._logistic(X)
		elif self._function == self.FUNCTIONS[2]:
			return self._tanh(X)
		elif self._function == self.FUNCTIONS[3]:
			return self._arctan(X)
		elif self._function == self.FUNCTIONS[4]:
			return self._softsign(X)
		elif self._function == self.FUNCTIONS[5]:
			return self._relu(X)

	def _relu(self, X):
		X[X < 0] = 0
		derivative_values = X > 0

		activated = X
		derivative = np.copy(X)
		derivative[derivative_values] = 1

		return activated, derivative

	def _softsign(self, X):
		activated = X / (1 + np.absolute(X))
		derivative = 1 / ((1 + np.absolute(X)) ** 2)

		return activated, derivative

	def _arctan(self, X):
		activated = np.arctan(X)
		derivative = 1 / (X ** 2 + 1)

		return activated, derivative

	def _tanh(self, X):
		activated = 2 / (1 + np.exp(-2 * X)) - 1
		derivative = 1 - activated ** 2

		return activated, derivative

	def _logistic(self, X):
		activated = 1 / (1 + np.exp(-X))
		derivative = activated * (1 - activated)

		return activated, derivative

	# Doesn't work for gradient descent so its not used
	def _binary_step(self, X):
		X[X >= 0] = 1.
		X[X < 0] = 0

		activated = X
		derivative = np.zeros(X.shape)

		return activated, derivative

	def _identity(self, X):
		activated = X
		derivative = np.ones(X.shape)

		return activated, derivative

	@staticmethod
	def softmax(X):
		for i in xrange(X.shape[0]):
			total = np.sum(X[i])

			for j in xrange(X.shape[1]):
				X[i][j] = np.exp(X[i][j]) / np.exp(total)