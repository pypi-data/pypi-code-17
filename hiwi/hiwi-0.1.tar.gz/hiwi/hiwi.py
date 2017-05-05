#!/usr/bin/python3 
# coding=utf-8

from zipfile import ZipFile
import numbers
import datetime
import ast
import os
import json
from .hiwierrors import *

class Hiwi:
	def __init__(self, settings_file="settings.py"):
		if not os.path.isfile(settings_file):
			raise SettingsFileNotFound(settings_file)

		self.settings_file = settings_file
		self.config_list = self._get_session_config_list()

		self.manifest_filename = "package-manifest.json"
		self.hiwi_version = "0.1"

		self.manifest = {
			"hiwi-version": "",
			"package-author": "",
			"created": "",
			"package-name": "",
			"session-config": {}
		}

	def package(self, name):
		self.manifest["package-name"] = name
		self.manifest["package-author"] = input("Author: ")
		self.manifest["created"] = datetime.datetime.utcnow().isoformat()
		self.manifest["hiwi-version"] = self.hiwi_version
		self.manifest["session-config"] = self._get_session_config(name)
		return self._zip()


	def integrate(self, zip_filepath):
		if not zip_filepath[:-4].lower() == ".zip":
			zip_filepath += ".zip"
		self.manifest = self._read_manifest(zip_filepath)
		self._unzip(zip_filepath)
		self.config_list.append(self.manifest["session-config"])
		self._write_otree_settings_file()


	def _write_otree_settings_file(self):
		with open(self.settings_file, 'r') as sfile:
			scontents = sfile.read()

		session_config_start = self._get_session_config_start_pos(scontents)
		session_config_end = self._get_session_config_end_pos(scontents)
		content_before_settings = scontents[:session_config_start]
		content_after_settings = scontents[session_config_end:]

		new_settings = content_before_settings + self._format_session_config_list() + content_after_settings

		with open(self.settings_file, 'w') as sfile:
			sfile.write(new_settings)

		return True



	def _format_session_config_list(self):
		indent_space = "    "
		indent_level = 1
		line_return = "\n"
		formated_session_config = "SESSION_CONFIGS = [" + line_return
		for session_config in self.config_list:
			formated_session_config += indent_space + "{" + line_return
			indent_level += 1
			for key, value in session_config.items():
				if isinstance(value, list): 
					formated_session_config += indent_level * indent_space + "\"" + key + "\": [" + line_return
					indent_level += 1
					for element in value:
						formated_session_config += indent_level * indent_space + self._ensure_string(element) + ", " + line_return
					indent_level -= 1
					formated_session_config += indent_level * indent_space + "]," + line_return
				else:
					formated_session_config += indent_level * indent_space + "\"" + key + "\": "+ self._ensure_string(value) + "," + line_return
				
			indent_level -= 1
			formated_session_config += indent_space + "}," + line_return
		formated_session_config += "]" + line_return


		return formated_session_config


	def _ensure_string(self, value):
		if isinstance(value, str):
			return "\""+value+"\""
		if isinstance(value, numbers.Number):
			return str(value)


	def _get_session_config(self, name):
		session_config = {}
		for config in self.config_list:
			if config['name'] == name:
				session_config = config
				break

		if not session_config:
			raise SessionConfigNotFound(name)

		return session_config


	def _get_session_config_start_pos(self, session_string):
		start_session_config = session_string.find("SESSION_CONFIGS = [")
		if start_session_config == -1:
			raise SessionConfigNotFound("SESSION_CONFIGS") # probably not the right error

		return start_session_config


	def _get_session_config_end_pos(self, session_config):
		bracket_counter = 0
		last_closing_pos = 0
		for pos, char in enumerate(session_config):
			if char == '[':
				bracket_counter += 1
			if char == ']':
				bracket_counter -= 1
				last_closing_pos = pos

		if bracket_counter != 0:
			raise IllFormatedSessionConfigs("brackets do not match")
		return last_closing_pos+1


	def _get_session_config_list(self):
		with open(self.settings_file, 'r') as sfile:
			scontents = sfile.read()

		start = self._get_session_config_start_pos(scontents)
		scontents = scontents[start + scontents[start:].find("["):]

		end = self._get_session_config_end_pos(scontents)
		scontents = scontents[:end]

		session_configs = ast.literal_eval(scontents)
		return session_configs


	def _zip(self):
		zip_filename = self.manifest["package-name"]+".zip"
		if os.path.isfile(zip_filename):
			raise FileExistsError(zip_filename)

		zip_file = ZipFile(zip_filename, "w")
		path_list = self._get_path_list(self.manifest["session-config"]["app_sequence"])
		zip_file.writestr(self.manifest_filename, json.dumps(self.manifest))
		for path in path_list:
			zip_file.write(path)
		zip_file.close()

		return zip_filename


	def _get_path_list(self, dir_list):
		path_list = []
		for folder in dir_list:
			if not os.path.isdir(folder):
				raise FileNotFoundError(folder)
			for root, subdirs, files in os.walk(folder, topdown=True):
				subdirs[:] = [ folder for folder in subdirs if not self._blacklisted(folder) ]
				for file in files:
					if not self._blacklisted(file):
						path_list.append(os.path.join(root, file))
		return path_list
						

	def _blacklisted(self, name):
		# more advanced would be to load blacklist from some file or online db
		blacklist = [
			"__pycache__",
			"_static",
			"_templates",
		]

		if name[0] == "." or name in blacklist:
			return True

		return False


	def _read_manifest(self, zip_filepath):
		if not os.path.isfile(zip_filepath):
			raise FileNotFoundError(zip_filepath)

		with ZipFile(zip_filepath, 'r') as zip_file:
			return json.loads(zip_file.read(self.manifest_filename).decode())


	def _unzip(self, zip_filepath):
		if not os.path.isfile(zip_filepath):
			raise FileNotFoundError(zip_filepath)

		target_dir_name = zip_filepath[:-4]
		if os.path.isdir(target_dir_name):
			raise FileExistsError(target_dir_name)

		with ZipFile(zip_filepath, 'r') as zip_file:
			members = [name for name in zip_file.namelist() if not name == self.manifest_filename]
			zip_file.extractall(".", members)

		return target_dir_name





# TODO
# - exception / error class
# - tests
# - hosted database of packages
# - publish script
# - find in db
# - integrate from web
# 