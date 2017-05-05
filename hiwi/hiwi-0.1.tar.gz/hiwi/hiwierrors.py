#!/usr/bin/python3 
# coding=utf-8

class Error(Exception):
	""" Base class """
	def __init__(self, message):
		self.message = message


class SettingsFileNotFound(Error):
	"""Exception raised if settings file is not found
	"""
	pass

class IllFormatedSessionConfigs(Error):
	pass

class SessionConfigNotFound(Error):
	pass

