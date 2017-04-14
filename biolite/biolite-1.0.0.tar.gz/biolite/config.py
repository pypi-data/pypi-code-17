# BioLite - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012 Brown University. All rights reserved.
#
# This file is part of BioLite.
#
# BioLite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BioLite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BioLite.  If not, see <http://www.gnu.org/licenses/>.

"""
Loads the entries in the *biolite.cfg* file into two member dictionaries,
`resources` (default parameters and data paths) and `tools` (paths to external
tools called by :ref:`wrappers`).

By default, BioLite will look for configuration files at the following
paths, in order of preference:

* the comma-separated values in the $BIOLITE_CONFIG environment variable
* $HOME/.biolite/biolite.cfg
* {install_prefix}/data/biolite.cfg

Individual resource and tool values can also be overridden with the environment
variables BIOLITE_RESOURCES and BIOLITE_TOOLS.

Finally, the GNU parallel wrapper is capable of running on multiple hosts, which can
be specified with the environment variable BIOLITE_HOSTLIST.
"""

import ConfigParser
import os
import shlex

import biolite
from biolite import utils

datadir = os.path.join(biolite.__path__[0], 'data')
uname = os.uname()[0]

resources = {}
tools = {}
parsed_paths = []


def parse(*paths):
	"""
	Parse the BioLite configuration files in `paths` in order, so that values
	in the later files override previous values.
	"""
	global resources, programs, parsed_paths
	parser = ConfigParser.ConfigParser(resources)
	for path in map(os.path.expanduser, paths):
		if os.path.isfile(path):
			parser.read(path)
			if parser.has_section('resources'):
				for key,val in parser.items('resources'):
					resources[key] = os.path.expanduser(val)
			if parser.has_section('tools'):
				for key,val in parser.items('tools'):
					tools[key] = os.path.expanduser(val)
			parsed_paths.append(path)


def parse_env_resources():
	"""
	Parse resources from a comma-separated string of key=val pairs in the
	environment variable BIOLITE_RESOURCES.
	"""
	global resources
	pairs = os.getenv('BIOLITE_RESOURCES')
	if pairs:
		for token in pairs.strip().split(','):
			pair = token.split('=')
			if len(pair) == 2:
				key, val = pair
				val = os.path.expanduser(val)
				if not resources.get(key) == val:
					resources[key] = val
					utils.info("%s=%s" % (key, val))
			else:
				utils.info("WARNING: invalid token '%s'" % token)


def parse_env_tools():
	"""
	Parse tools from a comma-separated string of key=val pairs in the
	environment variable BIOLITE_TOOLS.
	"""
	global tools
	pairs = os.getenv('BIOLITE_TOOLS')
	if pairs:
		for token in pairs.strip().split(','):
			pair = token.split('=')
			if len(pair) == 2:
				key, val = pair
				val = os.path.expanduser(val)
				if not tools.get(key) == val:
					tools[key] = val
					utils.info("%s=%s" % (key, val))
			else:
				utils.info("WARNING: invalid token '%s'" % token)


def parse_env_hostlist():
	"""
	Parse a hostlist from the environment variable BIOLITE_HOSTLIST. The
	hostlist is used for distributed processing in wrappers that use GNU
	parallel.
	"""
	global resources
	hostlist = os.getenv('BIOLITE_HOSTLIST')
	if hostlist:
		utils.info("hostlist=%s" % hostlist)
		resources['hostlist'] = hostlist


def get_env_paths(key):
	"""
	Return a list of paths split from a comma-separated list in the
	environment variable `key`.
	"""
	return os.getenv(key, "").split(',')


def get_resource(key):
	"""
	Lookup a resource from the configuration file for `key` and print
	an intelligble error message on KeyError.
	"""
	try:
		return resources[key]
	except KeyError:
		utils.die(
			"missing value for '%s' in your biolite.cfg at\n%s" % (
			key, resources.get('configpath', '[none found]')))


def get_resource_default(key, default):
	"""
	Lookup a resource from the configuration file for `key` and return the
	`default` value if the key is not found.
	"""
	return resources.get(key, default)


def get_command(key):
	"""
	Lookup the full path to the external tool `key` in the configuration file and
	print an intelligble error message if the path can't be found in the user's
	PATH environment variable (similar to the Unix utility `which`).

	The output is a list, starting with the full path to the tool, ready
	for input to subprocess.Popen. Any trailing parameters in config entry for
	the tool are preserved in this list.

	If there is no config entry for the key, or the entry is blank, the key is
	used as the name of the tool. Thus, the config file only needs to
	override tool paths that won't resolve correctly using PATH.
	"""
	tool = tools.get(key)
	if not tool:
		cmd = [key]
	else:
		cmd = shlex.split(tool)
	cmd[0] = utils.which(cmd[0])
	if not cmd[0]:
		if not tool:
			utils.info(
				"empty or missing tool '%s' in config file at:\n  %s" % (
					key, resources.get('configpath', '[biolite.cfg not found]')))
			tool = key
		utils.die(
			"couldn't find tool '%s' in your PATH:\n  %s" % (
				tool, '\n  '.join(os.environ["PATH"].split(os.pathsep))))
	return cmd


def set_database(path):
	"""
	Override the path to the BioLite database.
	"""
	if os.path.isdir(path):
		path = os.path.join(path, 'biolite.sqlite')
	if os.path.exists(path):
		resources['database'] = path
	else:
		utils.die("couldn't find BioLite database at:", path)


# Parse default and user config files automatically on module load.
parse(
	os.path.join(biolite.__path__[0], 'config', 'biolite.cfg'),
	'~/.biolite/biolite.cfg',
	*get_env_paths('BIOLITE_CONFIG'))
parse_env_resources()
parse_env_tools()
parse_env_hostlist()

# vim: noexpandtab ts=4 sw=4
