import os
from utils import *

"""
Usage: from BBB-LCDDisplay import BBB_GPIO
value: HIGH or LOW
direction: INPUT or OUTPUT
"""

class BBB_GPIO:
	"""
	Class for GPIO pin on Beaglebone black
	Init with name pin exemple: P8_44
	"""
	def __init__(self, pin):
		self.pin = self.__convert_pin(pin)
		self.gpio_path ='/sys/class/gpio/'
		self.pin_path = '{0}{1}/'.format(self.gpio_path, self.pin)
		self.__create()

	def __convert_pin(self, pin):
		"""Convert exemple P8_44 (name pin) on gpio73 (name kernel pin)"""
		try:
			return eval(pin)
		except NameError:
			print('Bad pin. Please choose an other!')

	def __open_directory(self, directory):
		"""Function to move in directory"""
		os.chdir(directory)

	def __cmd(self, arg, files):
		"""Fuction to set files by command"""
		os.system('sudo echo {0} > {1}'.format(arg, files))

	def __create(self):
		"""Create pin if it does'nt exist"""
		self.__open_directory(self.gpio_path)
		self.__cmd(self.pin[4:], 'export')

	def remove(self):
		"""Function to remove pin"""
		self.__open_directory(self.gpio_path)
		self.__cmd(self.pin[4:], 'unexport')

	def value(self, value):
		"""Fuction to set value of pin"""
		self.__open_directory(self.pin_path)
		if eval(str(value)) == '1' or '0':
			self.__cmd(eval(str(value)), 'value')
		else:
			raise Exception('Incorrect value, try with HIGH or LOW!')

	def direction(self, direction):
		"""Function to set IN or OUT pin"""
		self.__open_directory(self.pin_path)
		if direction == 'out' or 'in':
			self.__cmd(direction, 'direction')
		else:
			raise Exception('Incorrect direction, try with OUTPUT or INPUT')
