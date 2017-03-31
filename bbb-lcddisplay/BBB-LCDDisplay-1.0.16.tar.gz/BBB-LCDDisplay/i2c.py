import os
from fcntl import ioctl

"""
Not working but
Usage: from BBB-LCDDisplay import I2C
"""

class I2C:
	def __init__(self, address, port):
		"""Set address and port for i2c in Beaglebone black"""
		self.adress = address
		self.port = port
		self.i2c = os.open("/dev/i2c-{}".format(self.port), os.O_RDWR)

	def start_i2c(self):
		"""Setup i2c to start"""
		ioctl(self.i2c, 0x703, self.adress)

	def stop_i2c(self):
		"""Stop i2c"""
		os.close(self.i2c)

	def write(self, data):
		"""Write data"""
		os.write(self.i2c, bytes([data]))
