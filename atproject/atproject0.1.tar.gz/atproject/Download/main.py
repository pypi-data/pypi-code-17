#! /usr/bin/env python


from depend import run 
import time
import sys
import os.path as path
# from os import path
class CustomLibrary():

	def  __init__(self):
		self._torrent_path = ''
		self._download_path = ''


	@property
	def torrent_path(self):
		return self._torrent_path


	def torrent_path(self, value):
		self._torrent_path = value

	@property
	def download_path(self):
		return self._download_path


	def download_path(self, value):
		self._download_path = value



	def get(self):
		arguments = []
		# arguments.append(path.path(self.torrent_path))
		arguments.append(self.torrent_path)
		# print self.download_path

		# if self.download_path:
		# 	arguments.append('-saveas ' + self.download_path)

		run(arguments)