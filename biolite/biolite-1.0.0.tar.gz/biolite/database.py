# BioLite - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2017 Brown University. All rights reserved.
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
Provides an interface to the underlying SQLite database that stores the BioLite
**catalog**, **runs**, **diagnostics**, and **programs** tables.

.. _catalog-table:

catalog Table
-------------

::

%s

.. _runs-table:

runs Table
----------

::

%s

.. _diagnostics-table:

diagnostics Table
-----------------

::

%s

.. _store-table:

store Table
-----------------

::

%s

.. _programs-table:

programs Table
--------------

::

%s
"""

import atexit
import cPickle
import datetime
import os
import pandas as pd
import shutil
import sqlite3
import tempfile
import textwrap

import config
import utils


# Interal data and helper functions.
_db = None
_db_ramdisk = None
_db_ramdisk_path = None
_db_init_functions = []


def _create_sql(name, schema, index):
	sql = [" CREATE TABLE %s (" % name]
	sql += ["   %s %s," % s for s in schema[:-1]]
	sql += ["   %s %s);" % schema[-1]]
	sql += [" CREATE INDEX {0}_{1} ON {0}({1});".format(name, i) for i in index]
	return '\n'.join(sql)


def _create_db():
	global _db
	_db.execute("PRAGMA main.page_size=65536;")
	_db.executescript(catalog_sql + runs_sql + diagnostics_sql + store_sql + programs_sql)


# External data.
runs_schema = (
	("done", "INTEGER DEFAULT '0'"),
	("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
	("catalog_id", "VARCHAR(256)"),
	("name", "VARCHAR(32)"),
	("hostname", "VARCHAR(32)"),
	("username", "VARCHAR(32)"),
	("timestamp", "DATETIME"),
	("hidden", "INTEGER DEFAULT '0'"))

runs_index = ("catalog_id", "name", "done", "hidden")

runs_sql = _create_sql("runs", runs_schema, runs_index)

diagnostics_schema = (
	("catalog_id", "VARCHAR(256)"),
	("run_id", "INTEGER"),
	("entity", "VARCHAR(128)"),
	("attribute", "VARCHAR(32)"),
	("value", "TEXT"),
	("timestamp", "DATETIME"))
diagnostics_index = ("catalog_id", "run_id", "entity", "attribute", "timestamp")

diagnostics_sql = _create_sql("diagnostics", diagnostics_schema, diagnostics_index) + "CREATE UNIQUE INDEX diagnotics_entry ON diagnostics(run_id,entity,attribute);"

store_schema = (
	("run_id", "INTEGER"),
	("name", "VARCHAR(128)"),
	("pickled_value", "BLOB"),
	("timestamp", "DATETIME"))
store_index = ("run_id", "name", "timestamp")

store_sql = _create_sql("store", store_schema, store_index) + "CREATE UNIQUE INDEX store_entry ON store(run_id,name);"

catalog_schema = (
	("id", "VARCHAR(256) PRIMARY KEY NOT NULL"),
	("paths", "TEXT"),
	("species", "VARCHAR(256)"),
	("ncbi_id", "INTEGER"),
	("itis_id", "INTEGER"),
	("extraction_id", "VARCHAR(256)"),
	("library_id", "VARCHAR(256)"),
	("library_type", "VARCHAR(256)"),
	("individual", "VARCHAR(256)"),
	("treatment", "VARCHAR(256)"),
	("sequencer", "VARCHAR(256)"),
	("seq_center", "VARCHAR(256)"),
	("note", "TEXT"),
	("sample_prep", "TEXT"),
	("timestamp", "DATETIME"))

# Index all fields in the catalog, except id (already a key) and paths.
catalog_index = [column[0] for column in catalog_schema[2:]]
catalog_sql = _create_sql("catalog", catalog_schema, catalog_index)

programs_schema = (
	("binary", "CHAR(32) PRIMARY KEY NOT NULL"),
	("name", "VARCHAR(256)"),
	("version", "TEXT"))

programs_index = ("name",)
programs_sql = _create_sql("programs", programs_schema, programs_index)

# Add the SQL schema for each table to the documentation.
__doc__ %= (catalog_sql, runs_sql, diagnostics_sql, store_sql, programs_sql)


# Public functions. ###

def timestamp():
	"""
	Returns the current time in ISO 8601 format, e.g.
	:samp:`YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]`.
	"""
	return datetime.datetime.now().isoformat()


def connect():
	"""
	Establish a gobal database connection.
	"""
	global _db, _db_init_functions
	if _db is None:
		path = config.get_resource("database")
		if path is None:
			utils.die("no path provided for database file")
		exists = os.path.isfile(path)
		if not exists:
			utils.safe_mkdir(os.path.dirname(path))
		_db = sqlite3.connect(path, timeout=60.0, isolation_level=None)
		_db.row_factory = sqlite3.Row
		if not exists:
			_create_db()
		for func in _db_init_functions:
			func.__call__()


def disconnect():
	"""
	Close the global database connection, set it to None.
	"""
	global _db
	if _db is not None: _db.close()
	_db = None


def register_init(func):
	"""
	Add a function to be called when the first database
	connection is established.
	"""
	global _db_init_functions
	_db_init_functions.append(func)


def last_id():
	"""
	Call through to sqlite3.last_insert_rowid(); connects to database if not
	already connected.
	"""
	global _db
	if _db is None: connect()
	return _db.last_insert_rowid()


def execute(*args, **kwargs):
	"""
	Call through to sqlite3.execute; connects to database if not already
	connected.
	"""
	global _db
	if _db is None: connect()
	try:
		return _db.execute(*args, **kwargs)
	except sqlite3.InterfaceError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')
	except sqlite3.OperationalError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')


def executemany(*args, **kwargs):
	"""
	Call through to sqlite3.executemany; connects to database if not already
	connected.
	"""
	global _db
	if _db is None: connect()
	try:
		return _db.executemany(*args, **kwargs)
	except sqlite3.InterfaceError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1][0], "\n...\n")
	except sqlite3.OperationalError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1][0], "\n...\n")


def executescript(*args, **kwargs):
	"""
	Call through to sqlite3.executescript; connects to database if not already
	connected.
	"""
	global _db
	if _db is None: connect()
	try:
		return _db.executescript(*args, **kwargs)
	except sqlite3.InterfaceError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')
	except sqlite3.OperationalError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')


def executecolumn(i, *args, **kwargs):
	"""
	Call through to sqlite3.execute; connects to database if not already
	connected.

	Yields only the values from the column at index `i`, e.g. equivalent to:

	    map(itemgetter(i), execute(*args, **kwargs))

	"""
	global _db
	if _db is None: connect()
	try:
		for row in  _db.execute(*args, **kwargs):
			yield row[i]
	except sqlite3.InterfaceError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')
	except sqlite3.OperationalError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')


def store(run_id, name, value):
	"""
	Pickle and store the `value` in the database.

	http://stackoverflow.com/a/2340858
	"""
	pickled_value = cPickle.dumps(value, cPickle.HIGHEST_PROTOCOL)
	sql = "REPLACE INTO store VALUES(?,?,?,?);"
	execute(sql, (run_id, name, sqlite3.Binary(pickled_value), timestamp()))


def retrieve(run_id, name, quiet=False):
	"""
	Retrieve and unpickle the value for `name`.

	http://stackoverflow.com/a/2340858
	"""
	sql = "SELECT pickled_value FROM store WHERE run_id=? AND name=?;"
	pickled_value = execute(sql, (run_id, name)).fetchone()
	if pickled_value is None:
		if not quiet:
			utils.die("no stored entry for", name, "in run", run_id)
	else:
		return cPickle.loads(str(pickled_value[0]))


def connect_ramdisk():
	"""
	Copy the database to ramdisk and establish a gobal database connection.
	"""
	global _db_ramdisk, _db_ramdisk_path
	if _db_ramdisk is None:
		fileno, _db_ramdisk_path = tempfile.mkstemp(
							prefix="biolite-database-",
							dir=config.get_resource("ramdisk"))
		os.close(fileno)
		utils.info("copying database to ramdisk")
		shutil.copyfile(config.get_resource("database"), _db_ramdisk_path)
		_db_ramdisk = sqlite3.connect(_db_ramdisk_path, isolation_level=None)
		_db_ramdisk.row_factory = sqlite3.Row


@atexit.register
def disconnect_ramdisk():
	"""
	Close the global database connection, set it to None. Delete the ramdisk
	copy of the database.
	"""
	global _db_ramdisk, _db_ramdisk_path
	if _db_ramdisk is not None:
		_db_ramdisk.close()
		utils.info("removing database from ramdisk")
		os.remove(_db_ramdisk_path)
	_db_ramdisk = None
	_db_ramdisk_path = None


def execute_ramdisk(*args, **kwargs):
	"""
	Call through to sqlite3.execute; connects to an in-memory copy of the
	database if not already connected. The in-memory copy is stored in the
	ramdisk path specified in the BioLite resources list.
	"""
	global _db_ramdisk
	if _db_ramdisk is None: connect_ramdisk()
	try:
		return _db_ramdisk.execute(*args, **kwargs)
	except sqlite3.InterfaceError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')
	except sqlite3.OperationalError as e:
		utils.die(
			"sqlite error:\n", e, '\n',
			"SQL:", textwrap.dedent(args[0]), '\n',
			"Values:", args[1:], '\n')


def execute_dataframe(sql):
	"""
	Execute the `sql` statement and return the result as a pandas dataframe.
	"""
	global _db
	return pd.read_sql(sql, _db)


# vim: noexpandtab ts=4 sw=4
