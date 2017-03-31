import os

"""
Not working but
Usage: from BBB-LCDDisplay import Servo

For PWM:
polarity: 1 or 0
dutycicle: int(value)
frequence: int(value)
"""

class Servo:
	def __init__(self, pin):
		self.__create()

	def __create(self):
		"""Setup pin PWM. Please check PWM pin in BBB"""
		self.__open_directory('/lib/firmware/')
		self.__cmd('bone_pwm_P9_16', '/sys/devices/bone_capemgr*/slots')
		self.__open_directory('/sys/devices/ocp.3/pwm_test_P9_16.*')
		self.stop()

	def __open_directory(self, directory):
		"""Access directory"""
		os.chdir(directory)

	def __cmd(self, arg, files):
		"""Set command"""
		os.system('sudo echo {0} > {1}'.format(arg, files))

	def start(self):
		"""Start PWM for Servo"""
		self.__cmd(1, 'run')

	def stop(self):
		"""Stop PWM for Servo"""
		self.__cmd(0, 'run')

	def polarity(self, polarity):
		"""Set polarity PWM for Servo"""
		self.__cmd(polarity, 'polarity')

	def dutycicle(self, dutycycle):
		"""Set dutycicle PWM for Servo"""
		self.__cmd(dutycicle, 'duty')

	def frequence(self, frequence):
		"""Set frequence PWM for Servo"""
		self.__cmd(frequence, 'period')
