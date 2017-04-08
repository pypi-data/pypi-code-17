# -*- coding: utf-8 -*-
"""
Package Description

Engine Configuration
=================================================================================
The Engine is the starting point for any SQLAlchemy application. 
It’s “home base” for the actual database and its DBAPI, 
delivered to the SQLAlchemy application through a connection pool and a Dialect, 
which describes how to talk to a specific kind of database/DBAPI combination.

Supported Databases
---------------------------------------------------------------------------------
SQLAlchemy includes many Dialect implementations for various backends. 
Dialects for the most common databases are included with SQLAlchemy; 
a handful of others require an additional install of a separate dialect.
See the section Dialects for information on the various backends available.

Database Urls
---------------------------------------------------------------------------------
The create_engine() function produces an Engine object based on a URL. 
These URLs follow RFC-1738, and usually can include username, password, hostname, database name 
as well as optional keyword arguments for additional configuration. 
In some cases a file path is accepted, and in others a “data source name” replaces the “host” and “database” portions. 
The typical form of a database URL is:

dialect+driver://username:password@host:port/database

Dialect names include the identifying name of the SQLAlchemy dialect, 
a name such as sqlite, mysql, postgresql, oracle, or mssql. 
The drivername is the name of the DBAPI to be used to connect to the database using all lowercase letters. 
If not specified, a “default” DBAPI will be imported if available - this default is typically the most widely known driver available for that backend.

Examples for common connection styles follow below. 
For a full index of detailed information on all included dialects as well as links to third-party dialects, 
see Dialects.

PostgreSQL
---------------------------------------------------------------------------------
The PostgreSQL dialect uses psycopg2 as the default DBAPI. 
pg8000 is also available as a pure-Python substitute:
# default
engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
# psycopg2
engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')
# pg8000
engine = create_engine('postgresql+pg8000://scott:tiger@localhost/mydatabase')
More notes on connecting to PostgreSQL at PostgreSQL.

MySQL
---------------------------------------------------------------------------------
The MySQL dialect uses mysql-python as the default DBAPI. 
There are many MySQL DBAPIs available, including MySQL-connector-python and OurSQL:
# default
engine = create_engine('mysql://scott:tiger@localhost/foo')
# mysql-python
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
# MySQL-connector-python
engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')
# OurSQL
engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')
More notes on connecting to MySQL at MySQL.

Oracle
---------------------------------------------------------------------------------
The Oracle dialect uses cx_oracle as the default DBAPI:
engine = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')
engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')
More notes on connecting to Oracle at Oracle.

Microsoft SQL Server
---------------------------------------------------------------------------------
The SQL Server dialect uses pyodbc as the default DBAPI. pymssql is also available:
# pyodbc
engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')
# pymssql
engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
More notes on connecting to SQL Server at Microsoft SQL Server.

SQLite
---------------------------------------------------------------------------------
SQLite connects to file-based databases, using the Python built-in module sqlite3 by default.

As SQLite connects to local files, the URL format is slightly different. 
The “file” portion of the URL is the filename of the database. 
For a relative file path, 
this requires three slashes:

# sqlite://<nohostname>/<path>
# where <path> is relative:
engine = create_engine('sqlite:///foo.db')
And for an absolute file path, the three slashes are followed by the absolute path:
#Unix/Mac - 4 initial slashes in total
engine = create_engine('sqlite:////absolute/path/to/foo.db')
#Windows
engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
#Windows alternative using raw string
engine = create_engine(r'sqlite:///C:\path\to\foo.db')
To use a SQLite :memory: database, specify an empty URL:
engine = create_engine('sqlite://')
More notes on connecting to SQLite at SQLite.


Mongodb Configuration
=================================================================================
mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]


Redis Configuration
=================================================================================

"""
import os
import sys
import logging
import json

NIMBUS_DEFAULT_NAME = "default"

NIMBUS_SETTING_CLIENT_DB = "NIMBUS_DATABASE"
NIMBUS_SETTING_CLIENT_MONGODB = "NIMBUS_MONGODB"
NIMBUS_SETTING_CLIENT_REDIS = "NIMBUS_REDIS"

DEFAULT_DATABASE_SQLITE = {
    "db_uri": "{dialect}{db}",
    "dialect": "sqlite://",
    "convert_unicode": True,
    "encoding": "utf-8",
    "autocommit": False,
    "autoflush": False,
    "autocreate": True,
}

DEFAULT_DATABASE = {
    "db_uri": "{dialect}{user}:{password}@{host}:{port}/{db}",
    "dialect": "mysql+mysqlconnector://",
    "host": "xxx.xxx.xxx.xxx",
    "port": "3306",
    "db": "xxx",
    "user": "xxx",
    "password": "xxx",
    "echo": False,
    "encoding": "utf-8",
    "pool_recycle": 800,
    "autocommit": False,
    "autoflush": False,
}

DEFAULT_REDIS = {
    "host": '127.0.0.1',
    "port": 6379,
    "db": 0,
    "password": None,
}

DEFAULT_MONGODB = {
    "uri": "mongodb://127.0.0.1:27017/",
    "db": "default",
}



