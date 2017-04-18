# -*- coding: utf-8 -*-

# =============================================================
# Author: http://aleskrejci.cz
# =============================================================

import os
import errno
from random import choice
from shutil import rmtree
from tempfile import gettempdir


TMP_MAX = 10000  # Try again, max number


def notremoved(tempdir):
	from platform import system
	from subprocess import call

	if system() == "Windows":
		'''
		CMD [/A | /U] [/Q] [/D] [/E:ON | /E:OFF] [/F:ON | /F:OFF] [/V:ON | /V:OFF] [[/S] [/C | /K] string]
		/C      Carries out the command specified by string and then terminates
		/S      Modifies the treatment of string after /C or /K (see below)
		/Q      Turns echo off
		'''
		try:
			call(['cmd', '/C', 'rmdir', '/S', '/Q', tempdir], shell=False)
		except Exception as e:
			pass

	if os.path.exists(tempdir):
		return True
	return False


class TemporaryDirectoryWrapper:
	def __init__(self, tempdir, auto_delete=True):
		self.tempdir = tempdir
		self._is_autodelete = auto_delete

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		if self._is_autodelete:
			self.remove()

	def __del__(self):
		if self._is_autodelete:
			self.remove()

	def rmtemp(self):
		# NOTE: Backward compatibility
		self.remove()

	def remove(self):
		if os.path.exists(self.tempdir):
			try:
				rmtree(self.tempdir)
			except Exception as e:
				if e.errno == errno.EACCES:
					if notremoved(self.tempdir):
						raise IOError(errno.EACCES, 'Cannot remove temporary directory "{}".'.format(self.tempdir))
				else:
					raise e

	@property
	def name(self):
		return self.tempdir


def generate_random_chain(length=12):
	characters = {
		'letters': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
		'digits': '0123456789'
	}

	all_chars = ''.join(str(x) for x in characters.values())  # All the characters in one variable
	rand_chars = ''.join(choice(all_chars) for x in range(length))  # Generate random characters
	return rand_chars


def TemporaryDirectory(suffix='', prefix='', dir=None, delete=True):
	if not dir or dir is None:
		dir = gettempdir()

	if not os.path.exists(dir):
		raise IOError(errno.EEXIST, 'Directory "{}" not exists.'.format(dir))

	tempdir = None
	for i in range(TMP_MAX, 0, -1):
		tempdir = os.path.join(dir, prefix + generate_random_chain() + suffix)
		try:
			os.mkdir(tempdir)
		except OSError as e:
			if e.errno == errno.EEXIST:
				continue  # If folder exists, try again.
			else:
				raise e
		else:
			return TemporaryDirectoryWrapper(tempdir, delete)

	if tempdir:
		raise IOError(errno.EEXIST, 'Cannot create temporary directory "{}".'.format(tempdir))
	raise IOError(errno.EEXIST, 'Cannot create temporary directory in "{}".'.format(dir))
