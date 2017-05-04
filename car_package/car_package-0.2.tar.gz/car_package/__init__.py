class Car(object):
	"""This creates a Car class. It's methods dictate what you
	can do with the car from starting it to filling it with gas."""
	def __init__(self, make, model):
		self.make = make
		self.model = model

	def startCar(self):
		print('Vrooooooom!!!!')
		# will print car start sound

	def drive(self, speed=0.0):
		"""Speed should be a numeric value.
		>>> drive(55)
		55
		>>> drive(73.2)
		73.2
		"""
		if speed > 150:
			raise RuntimeError('Car cannot go faster than 150 mph.')
		self.speed = speed